# services/upstox/feed_manager.py

import asyncio
import json
import ssl
import logging
import websockets
import requests

from google.protobuf.json_format import MessageToDict
from services.upstox.MarketDataFeed_pb2 import FeedResponse

logger = logging.getLogger(__name__)


class UpstoxFeedManager:
    def __init__(self):
        self.websocket = None
        self.access_token = None
        self.clients = []
        self.connected = False

    async def initialize(self, access_token, client_ws):
        self.access_token = access_token
        self.clients.append(client_ws)

        if not self.connected:
            asyncio.create_task(self._connect_websocket())

    async def _connect_websocket(self):
        try:
            ws_url = self._get_authorized_ws_url()

            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE

            async with websockets.connect(ws_url, ssl=ssl_context) as ws:
                self.websocket = ws
                self.connected = True
                logger.info("✅ Connected to Upstox WebSocket")

                async for message in ws:
                    decoded = self._decode_protobuf(message)

                    if decoded.get("type") == "market_info":
                        await self._broadcast(
                            {"type": "market_info", "status": decoded}
                        )
                    elif decoded.get("type") == "live_feed":
                        await self._broadcast(
                            {"type": "live_feed", "data": decoded.get("feeds", {})}
                        )

        except Exception as e:
            logger.error(f"❌ WebSocket Upstox Error: {e}")

    async def subscribe_to_instruments(self, instrument_keys: list, client_ws):
        if client_ws not in self.clients:
            self.clients.append(client_ws)

        # ✅ Send JSON-encoded binary message (your original logic)
        data = {
            "guid": "some-guid",
            "method": "sub",
            "data": {"mode": "full", "instrumentKeys": instrument_keys},
        }
        binary_data = json.dumps(data).encode("utf-8")
        try:
            await self.websocket.send(binary_data)
        except Exception as e:
            logger.error(f"❌ Subscription error: {e}")

    async def _broadcast(self, payload: dict):
        disconnected = []
        for ws in self.clients:
            try:
                await ws.send_json(payload)
            except Exception:
                disconnected.append(ws)
        for ws in disconnected:
            self.clients.remove(ws)

    def _decode_protobuf(self, message):
        feed = FeedResponse()
        feed.ParseFromString(message)
        return MessageToDict(feed)

    def _get_authorized_ws_url(self):
        url = "https://api.upstox.com/v3/feed/market-data-feed/authorize"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Accept": "application/json",
        }
        res = requests.get(url, headers=headers)
        return res.json()["data"]["authorized_redirect_uri"]


upstox_feed_manager = UpstoxFeedManager()
