from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List
from datetime import datetime
from app.db import Database
from app.utils import ConnectionManager, FibonacciRequest, JSONResponse
from app.fibonacci import fib_async
from pydantic import ValidationError
from contextlib import asynccontextmanager
import asyncio
manager = ConnectionManager()
db = Database("sqlite+aiosqlite:///./Usuarios.db")

@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.init_db()  # <- Cria a tabela se necessário
    asyncio.create_task(manager.broadcast_time())
    yield

app = FastAPI(lifespan=lifespan)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    await db.add_user(str(websocket.client))
    try:
        while True:
            data = await websocket.receive_text()
            try:
                req = FibonacciRequest.parse_raw(data)
                if req.command == "fibonacci":
                    result = await fib_async(req.value)
                    await websocket.send_text(JSONResponse(result))
                else:
                    await websocket.send_text("Comando desconhecido.")
            except ValidationError:
                await websocket.send_text("Erro: JSON inválida. Envie no formato correto.")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await db.remove_user(str(websocket.client))
    except Exception as e:
        await websocket.send_text(f"Erro: {str(e)}")
        manager.disconnect(websocket)
        await db.remove_user(str(websocket.client))
