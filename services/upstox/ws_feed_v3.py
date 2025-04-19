import asyncio
import json
import ssl
import requests
import websockets
import logging
from datetime import datetime, timedelta
from typing import List, Optional

from google.protobuf.json_format import MessageToDict
from services.upstox import MarketDataFeed_pb2 as pb
from services.upstox.ws_manager import UpstoxWebSocketManager
from database.connection import get_db
from database.models import User
from router.upstox_router import refresh_upstox_token

logger = logging.getLogger(__name__)


class UpstoxWebSocketClient:
    def __init__(self, ws_manager: UpstoxWebSocketManager):
        self.ws_manager = ws_manager
        self.access_token: Optional[str] = None
        self.instrument_keys: List[str] = []
        self.user_email: Optional[str] = None
        self.websocket = None
        self.is_connected = False

    def get_access_token(self, user_email: str) -> str:
        db = next(get_db())
        user: User = db.query(User).filter(User.email == user_email).first()
        if not user:
            raise Exception("User not found")

        broker = next(
            (b for b in user.broker_configs if b.broker_name.lower() == "upstox"), None
        )
        if not broker or not broker.access_token:
            raise Exception("Upstox not linked or access token missing")

        if broker.access_token_expiry and broker.access_token_expiry < datetime.now():
            logger.info("🔁 Refreshing Upstox access token...")
            token_data = refresh_upstox_token(broker.refresh_token)
            broker.access_token = token_data["access_token"]
            broker.refresh_token = token_data.get("refresh_token", broker.refresh_token)
            broker.access_token_expiry = datetime.now() + timedelta(
                seconds=token_data.get("expires_in", 86400)
            )
            db.commit()

        return broker.access_token

    def decode_protobuf(self, buffer):
        feed_response = pb.FeedResponse()
        feed_response.ParseFromString(buffer)
        return feed_response

    async def start(self, user_email: str, instrument_keys: List[str]):
        self.stop_flag = False
        self.user_email = user_email
        self.instrument_keys = instrument_keys
        self.access_token = self.get_access_token(user_email)

        try:
            response = requests.get(
                url="https://api.upstox.com/v3/feed/market-data-feed/authorize",
                headers={"Authorization": f"Bearer {self.access_token}"},
            )
            response.raise_for_status()
            ws_url = response.json()["data"]["authorized_redirect_uri"]
            logger.info(f"🔗 Authorized WebSocket URL: {ws_url}")

            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE

            async with websockets.connect(ws_url, ssl=ssl_context) as websocket:
                logger.info("✅ Upstox WebSocket connected")
                self.websocket = websocket

                await self.send_subscription(websocket)

                while not self.stop_flag:
                    try:
                        raw_msg = await asyncio.wait_for(websocket.recv(), timeout=30)
                        decoded_msg = self.decode_protobuf(raw_msg)
                        parsed = MessageToDict(decoded_msg)

                        # 🟡 Handle Market Info
                        if parsed.get("type") == "market_info":
                            market_info = parsed.get("marketInfo", {})
                            logger.info(
                                f"📶 Market Info: {json.dumps(market_info, indent=2)}"
                            )

                            # ✅ Market Closed Check (send only once)
                            if not self.market_closed_sent:
                                segment_status = market_info.get("segmentStatus", {})
                                all_closed = all(
                                    v in ["NORMAL_CLOSE", "CLOSING_END"]
                                    for v in segment_status.values()
                                )
                                if all_closed:
                                    await self.ws_manager.broadcast_feed(
                                        self.user_email,
                                        json.dumps(
                                            {
                                                "event": "market_closed",
                                                "message": "Market is closed.",
                                            }
                                        ).encode(),
                                    )
                                    self.market_closed_sent = True
                                    logger.warning("🔒 Market closed. Stopping feed.")
                                    break  # disconnect loop
                            continue

                        # 🟢 Handle Feed Data
                        if isinstance(parsed.get("feeds"), dict):
                            feeds = parsed["feeds"]

                            for instrument_key, feed_data in feeds.items():
                                market_ff = feed_data.get("fullFeed", {}).get(
                                    "marketFF", {}
                                ) or feed_data.get("firstLevelWithGreeks", {})

                                ltpc = market_ff.get("ltpc", {})
                                ltp = ltpc.get("ltp")
                                ltt = ltpc.get("ltt")
                                atp = market_ff.get("atp")
                                vtt = market_ff.get("vtt")
                                depth = market_ff.get("marketLevel", {}).get(
                                    "bidAskQuote", []
                                )

                                is_market_closed = not depth or all(
                                    not level for level in depth
                                )

                                if ltp is None:
                                    logger.warning(
                                        f"⚠️ No LTP for {instrument_key}, skipping tick."
                                    )
                                    continue

                                try:
                                    timestamp = datetime.fromtimestamp(
                                        int(ltt) / 1000.0
                                    ).isoformat()
                                except Exception:
                                    timestamp = ltt

                                logger.info(
                                    f"📊 [{instrument_key}] LTP: ₹{ltp} | ATP: {atp} | Vol: {vtt} | Time: {timestamp}"
                                )

                                self.snapshot_sent = True

                                await self.ws_manager.broadcast_feed(
                                    self.user_email,
                                    json.dumps(
                                        {
                                            "instrument_key": instrument_key,
                                            "data": {
                                                "ltp": ltp,
                                                "avg_price": atp,
                                                "timestamp": timestamp,
                                                "volume": vtt,
                                                "depth": depth,
                                                "market_closed": is_market_closed,
                                            },
                                        }
                                    ).encode(),
                                )

                    except asyncio.TimeoutError:
                        await websocket.send(json.dumps({"method": "ping"}))
                    except Exception as e:
                        logger.error(f"❌ Error in receiving message: {str(e)}")
                        break

        except Exception as e:
            logger.error(f"❌ Failed to connect to Upstox WebSocket: {str(e)}")

        logger.info("🔌 Upstox WebSocket closed")

    async def send_subscription(self, websocket):
        payload = {
            "guid": "algo-terminal",
            "method": "sub",
            "data": {"mode": "full", "instrumentKeys": self.instrument_keys},
        }
        await websocket.send(json.dumps(payload).encode("utf-8"))
        logger.info(f"📨 Subscribed to: {self.instrument_keys}")

    async def subscribe_to_new_instruments(self, new_keys: List[str]):
        if not self.websocket:
            logger.warning("⚠️ WebSocket not connected. Cannot subscribe.")
            return

        new_unique_keys = list(set(self.instrument_keys + new_keys))
        if set(new_unique_keys) == set(self.instrument_keys):
            logger.info("🟡 No new keys to subscribe.")
            return

        self.instrument_keys = new_unique_keys
        await self.send_subscription(self.websocket)
        logger.info(f"🆕 Subscribed to additional instruments: {new_keys}")

    def stop(self):
        self.stop_flag = True
