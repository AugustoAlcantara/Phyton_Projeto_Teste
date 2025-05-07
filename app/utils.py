import asyncio
import json
from fastapi import WebSocket
from typing import List
from datetime import datetime, timezone
from pydantic import BaseModel

class CalculoFibonacci(BaseModel):
    command: str
    value: int

class GestorDeConecxao:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def conectar(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def desconectar(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def transmitir_horario(self):
        while True:
            now = datetime.now(timezone.utc).isoformat()
            for conn in list(self.active_connections):
                try:
                    await conn.send_text(json.dumps({"datetime": now}))
                except Exception:
                    self.disconnect(conn)
            await asyncio.sleep(1)

def JSONResponse(result: int) -> str:
    return json.dumps({"fibonacci": result})
