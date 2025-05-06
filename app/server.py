import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List
from datetime import datetime
from app.db import Database
from app.fibonacci import fib_async
from app.utils import ConnectionManager, FibonacciRequest, JSONResponse

app = FastAPI()
manager = ConnectionManager()
db = Database("sqlite+aiosqlite:///./connected_users.db")

@app.on_event("startup")
async def startup():
    await db.init_db()
    # inicia o broadcast de horário
    asyncio.create_task(manager.broadcast_time())

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    await db.add_user(str(websocket.client))
    try:
        while True:
            data = await websocket.receive_text()
            req = FibonacciRequest.parse_raw(data)
            if req.command == "fibonacci":
                result = await fib_async(req.value)
                await websocket.send_text(JSONResponse(result))
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await db.remove_user(str(websocket.client))