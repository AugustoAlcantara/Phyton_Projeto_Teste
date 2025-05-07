from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List
from datetime import datetime
from app.db import Database
from app.utils import GestorDeConecxao, CalculoFibonacci, JSONResponse
from app.fibonacci import calculoFib
from pydantic import ValidationError
from contextlib import asynccontextmanager
import asyncio
manager = GestorDeConecxao()
db = Database("sqlite+aiosqlite:///./Usuarios.db")

@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.init_db() 
    asyncio.create_task(manager.transmitir_horario())
    yield

app = FastAPI(lifespan=lifespan)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.conectar(websocket)
    await db.add_user(str(websocket.client))
    try:
        while True:
            data = await websocket.receive_text()
            try:
                req = CalculoFibonacci.parse_raw(data)
                if req.command == "fibonacci":
                    result = await calculoFib(req.value)
                    await websocket.send_text(JSONResponse(result))
                else:
                    await websocket.send_text("Comando desconhecido.")
            except ValidationError:
                await websocket.send_text("Erro: JSON inválida. Envie no formato correto.")
    except WebSocketDisconnect:
        manager.desconectar(websocket)
        await db.remove_user(str(websocket.client))
    except Exception as e:
        await websocket.send_text(f"Erro: {str(e)}")
        manager.desconectar(websocket)
        await db.remove_user(str(websocket.client))
