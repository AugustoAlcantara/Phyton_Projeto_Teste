import json
from fastapi import WebSocket
from typing import List
from datetime import datetime
from pydantic import BaseModel

class FibonacciRequest(BaseModel):
    command: str
    value: int

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast_time(self):
        while True:
            now = datetime.utcnow().isoformat()
            for conn in list(self.active_connections):
                await conn.send_text(json.dumps({"datetime": now}))
            await asyncio.sleep(1)

def JSONResponse(result: int) -> str:
    return json.dumps({"fibonacci": result})
