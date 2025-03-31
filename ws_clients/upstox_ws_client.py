import asyncio
import json
import logging
import websockets

logger = logging.getLogger(__name__)

class UpstoxWebSocketClient:
    def __init__(self, token: str, instruments: list, on_message):
        self.token = token
        self.instruments = instruments
        self.url = "wss://api.upstox.com/v3/feed/market-data-feed"
        self.on_message = on_message

    async def connect(self):
        headers = {
            "Authorization": f"Bearer {self.token}"
        }

        try:
            async with websockets.connect(self.url, extra_headers=headers) as websocket:
                logger.info("✅ Connected to Upstox WebSocket")

                # Send subscription
                subscribe_message = {
                    "guid": "abc123",
                    "method": "sub",
                    "data": {
                        "mode": "ltpc",
                        "instrumentKeys": self.instruments
                    }
                }

                await websocket.send(json.dumps(subscribe_message))
                logger.info(f"📩 Subscribed to: {self.instruments}")

                # Listen to incoming messages
                while True:
                    try:
                        msg = await websocket.recv()

                        # 👇 For now assume it's JSON (Upstox may send Protobuf, we'll decode later)
                        data = json.loads(msg)
                        await self.on_message(data)

                    except Exception as e:
                        logger.error(f"⛔ Error receiving from Upstox: {str(e)}")
                        break

        except Exception as e:
            logger.error(f"❌ Failed to connect to Upstox WebSocket: {str(e)}")
