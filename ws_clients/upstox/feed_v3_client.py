import asyncio
import json
import ssl
import websockets
import requests
import logging
from google.protobuf.json_format import MessageToDict
from proto import market_data_pb2 as pb
from fastapi import WebSocket

logger = logging.getLogger(__name__)


class UpstoxFeedClient:
    def __init__(self, access_token: str):
        self.access_token = access_token
        self.websocket = None
        self.ssl_context = self._create_ssl_context()
        self.instrument_keys = set()
        self.is_connected = False
        self.frontend_clients = {}  # { instrumentKey: set of WebSocket clients }

    def _create_ssl_context(self):
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        return ctx

    def get_authorized_ws_url(self):
        headers = {"Authorization": f"Bearer {self.access_token}"}
        response = requests.get(
            "https://api.upstox.com/v3/feed/market-data-feed/authorize",
            headers=headers,
        )
        response.raise_for_status()
        return response.json()["data"]["authorized_redirect_uri"]

    async def connect(self):
        url = self.get_authorized_ws_url()
        self.websocket = await websockets.connect(url, ssl=self.ssl_context)
        self.is_connected = True
        logger.info("✅ Connected to Upstox Market Feed V3")

        asyncio.create_task(self._receive_loop())

    async def _receive_loop(self):
        try:
            while self.is_connected:
                raw_data = await self.websocket.recv()
                response = pb.FeedResponse()
                response.ParseFromString(raw_data)
                message_dict = MessageToDict(response)

                if "ltpc" in message_dict:
                    for tick in message_dict["ltpc"]:
                        instrument_key = tick["instrumentKey"]
                        if instrument_key in self.frontend_clients:
                            for ws in list(self.frontend_clients[instrument_key]):
                                try:
                                    await ws.send_json(
                                        {"instrument_key": instrument_key, "data": tick}
                                    )
                                except Exception as e:
                                    logger.warning(
                                        f"⚠️ Failed to send LTP to client: {e}"
                                    )
                                    self.remove_client(ws)
        except Exception as e:
            logger.error(f"❌ Upstox receive loop error: {e}")
            self.is_connected = False

    async def subscribe(self, instrument_key: str, websocket: WebSocket):
        # Track user WebSocket
        if instrument_key not in self.frontend_clients:
            self.frontend_clients[instrument_key] = set()

        self.frontend_clients[instrument_key].add(websocket)

        if instrument_key not in self.instrument_keys:
            self.instrument_keys.add(instrument_key)
            if self.is_connected:
                payload = {
                    "guid": "market_feed",
                    "method": "sub",
                    "data": {
                        "mode": "full",
                        "instrumentKeys": list(self.instrument_keys),
                    },
                }
                await self.websocket.send(json.dumps(payload).encode("utf-8"))
                logger.info(f"📨 Subscribed to {instrument_key}")

    def remove_client(self, websocket: WebSocket):
        for key in list(self.frontend_clients.keys()):
            if websocket in self.frontend_clients[key]:
                self.frontend_clients[key].remove(websocket)
                logger.info(f"🧹 Removed client from {key}")
                if not self.frontend_clients[key]:
                    del self.frontend_clients[key]

    async def close(self):
        self.is_connected = False
        if self.websocket:
            await self.websocket.close()
            logger.info("🔌 Upstox feed WebSocket closed")
