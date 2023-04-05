from typing import List
from fastapi import WebSocket
from fastapi import APIRouter

router = APIRouter()


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    @staticmethod
    async def send_personal_message(message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast_message(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

    @staticmethod
    async def send_personal_bytes(_bytes: bytes, websocket: WebSocket):
        await websocket.send_bytes(_bytes)

    @staticmethod
    async def send_personal_json(message: dict, websocket: WebSocket):
        await websocket.send_json(message)


manager = ConnectionManager()
