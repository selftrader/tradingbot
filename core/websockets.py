from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List
import logging

router = APIRouter()
logger = logging.getLogger("uvicorn")

class ConnectionManager:
    """Manages active WebSocket connections"""
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        """Accepts a new WebSocket connection"""
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"🔗 New client connected. Total connections: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        """Removes a WebSocket connection"""
        self.active_connections.remove(websocket)
        logger.info(f"🔌 Client disconnected. Total connections: {len(self.active_connections)}")

    async def broadcast(self, message: dict):
        """Sends a message to all connected clients"""
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except:
                self.disconnect(connection)

# Initialize WebSocket manager
manager = ConnectionManager()

@router.websocket("/ws/trades")
async def websocket_endpoint(websocket: WebSocket):
    """Handles real-time trade updates via WebSocket"""
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()  # Keep connection alive
    except WebSocketDisconnect:
        manager.disconnect(websocket)
