import asyncio
import json
import ssl
import websockets
from google.protobuf.json_format import MessageToDict
import proto.market_data_pb2 as pb
import logging

logger = logging.getLogger("stock_logger")


class UpstoxWebSocketClient:
    def __init__(self):
        self.running = False
        self.access_token = None
        self.ws = None
        self.instrument_keys = []

    def set_token(self, token: str):
        self.access_token = token

    def get_feed_url(self):
        import requests

        headers = {"Authorization": f"Bearer {self.access_token}"}
        res = requests.get(
            "https://api.upstox.com/v3/feed/market-data-feed/authorize", headers=headers
        )
        return res.json()["data"]["authorized_redirect_uri"]

    async def start_feed(self, instrument_keys):
        if self.running:
            return
        self.running = True
        self.instrument_keys = instrument_keys

        try:
            url = self.get_feed_url()
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE

            async with websockets.connect(url, ssl=ssl_context) as websocket:
                self.ws = websocket
                logger.info("📡 Upstox WebSocket connected")

                payload = {
                    "guid": "dashboard-feed",
                    "method": "sub",
                    "data": {"mode": "full", "instrumentKeys": self.instrument_keys},
                }

                await websocket.send(json.dumps(payload).encode("utf-8"))

                while True:
                    message = await websocket.recv()
                    decoded = pb.FeedResponse()
                    decoded.ParseFromString(message)
                    data = MessageToDict(decoded)
                    await self.broadcast(data)

        except Exception as e:
            self.running = False
            logger.error(f"❌ Feed error: {e}")

    # Broadcast to connected UI clients
    async def broadcast(self, data):
        for client in self.clients.copy():
            try:
                await client.send_json({"type": "live_feed", "data": data})
            except Exception:
                self.clients.remove(client)

    # WebSocket clients list (injected by market_ws.py)
    clients = []


# Singleton instance
upstox_ws_client = UpstoxWebSocketClient()
