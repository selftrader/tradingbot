from typing import Dict, List
from fastapi import WebSocket
import logging

logger = logging.getLogger(__name__)


class UpstoxWebSocketManager:
    def __init__(self):
        self.connections: Dict[str, List[WebSocket]] = {}
        self.instrument_subscriptions: Dict[WebSocket, List[str]] = {}

    async def connect(
        self, user_email: str, websocket: WebSocket, instrument_keys: List[str]
    ):
        if user_email not in self.connections:
            self.connections[user_email] = []
        self.connections[user_email].append(websocket)
        self.instrument_subscriptions[websocket] = instrument_keys
        logger.info(f"📲 Connection added for {user_email}")

    async def disconnect(self, user_email: str, websocket: WebSocket):
        if user_email in self.connections:
            self.connections[user_email] = [
                ws for ws in self.connections[user_email] if ws != websocket
            ]
            if not self.connections[user_email]:
                del self.connections[user_email]
        if websocket in self.instrument_subscriptions:
            del self.instrument_subscriptions[websocket]
        logger.info(f"🔌 Disconnected {user_email}")

    def has_active_connection(self, user_email: str) -> bool:
        return user_email in self.connections and len(self.connections[user_email]) > 0

    async def broadcast_feed(self, user_email: str, message: bytes):
        text_message = message.decode()
        connections = self.connections.get(user_email, [])
        disconnected = []

        for ws in connections:
            try:
                await ws.send_text(text_message)
            except Exception as e:
                logger.error(f"❌ Error sending message to {user_email}: {e}")
                disconnected.append(ws)

        for ws in disconnected:
            await self.disconnect(user_email, ws)

    def get_active_connections_count(self) -> int:
        return sum(len(conn_list) for conn_list in self.connections.values())

    def get_subscribed_instruments_count(self) -> int:
        return sum(len(keys) for keys in self.instrument_subscriptions.values())
