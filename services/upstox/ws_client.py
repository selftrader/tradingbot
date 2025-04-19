import asyncio, json, ssl, logging, functools, inspect, requests, websockets
from websockets.exceptions import InvalidStatus
from google.protobuf.json_format import MessageToDict
import services.upstox.MarketDataFeed_pb2 as pb

logger = logging.getLogger("ws_client")

received_ltp = False  # ✅ Flag to track if LTP was received


def sync_fetch_feed_url(access_token: str):
    url = "https://api.upstox.com/v3/feed/market-data-feed/authorize"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(url, headers=headers)
    return response.json()


class UpstoxWebSocketClient:
    def __init__(
        self,
        access_token,
        instrument_keys,
        callback,
        stop_callback=None,
        on_auth_error=None,
        max_retries=5,
    ):
        self.access_token = access_token
        self.instrument_keys = instrument_keys
        self.callback = callback
        self.stop_callback = stop_callback
        self.on_auth_error = on_auth_error
        self.websocket = None
        self.should_run = True
        self.retry_count = 0
        self.max_retries = max_retries
        self.auth_error_sent = False
        self.last_ws_url = None
        self.market_closed = False  # ✅ Flag if market is closed
        self.received_ltp = False  # ✅ Flag if LTP was received

    async def get_feed_authorized_url(self):
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None, functools.partial(sync_fetch_feed_url, self.access_token)
        )
        logger.info(f"🔐 Feed Auth Response: {result}")
        if result.get("status") != "success":
            if self.on_auth_error and not self.auth_error_sent:
                await self.on_auth_error()
                self.auth_error_sent = True
            raise PermissionError("Access token expired")

        new_url = result["data"]["authorized_redirect_uri"]
        if new_url == self.last_ws_url:
            logger.warning("⚠️ Reused WebSocket URL detected, skipping.")
            raise InvalidStatus(403)
        self.last_ws_url = new_url
        return new_url

    async def connect_and_stream(self):
        while self.should_run and self.retry_count <= self.max_retries:
            try:
                ws_url = await self.get_feed_authorized_url()
                ssl_context = ssl.create_default_context()
                ssl_context.check_hostname = False
                ssl_context.verify_mode = ssl.CERT_NONE

                async with websockets.connect(ws_url, ssl=ssl_context) as conn:
                    self.websocket = conn
                    self.retry_count = 0
                    self.auth_error_sent = False
                    self.market_closed = False
                    self.received_ltp = False

                    logger.info("✅ WebSocket connected.")
                    await self._send_subscription()

                    while self.should_run:
                        raw = await conn.recv()
                        msg = pb.FeedResponse()
                        msg.ParseFromString(raw)
                        parsed = MessageToDict(msg)

                        msg_type = parsed.get("type")
                        logger.debug(f"📥 Tick Received: {parsed}")

                        if msg_type == "market_info":
                            status = (
                                parsed.get("marketInfo", {})
                                .get("segmentStatus", {})
                                .get("NSE_EQ", "")
                            )
                            logger.info(f"📊 Market status: {status}")
                            await self.callback(
                                {"type": "market_info", "status": status}
                            )
                            if (
                                status in ["NORMAL_CLOSE", "CLOSING_END"]
                                and self.received_ltp
                            ):
                                logger.info(
                                    "📴 Market is closed and LTP received. Stopping."
                                )
                                self.market_closed = True

                        elif msg_type == "ltpc":
                            symbol = parsed.get("symbol") or parsed.get("ltpc", {}).get(
                                "symbol"
                            )
                            if not symbol:
                                logger.warning("⚠️ Missing symbol in tick")
                                continue

                            self.received_ltp = True
                            logger.info(f"✅ Calling callback for symbol {symbol}")
                            await self.callback(
                                {"type": "live_feed", "data": {symbol: parsed}}
                            )

                            if self.market_closed:
                                logger.info(
                                    "📴 Market is closed & LTP received. Stopping."
                                )
                                self.should_run = False
                        elif "feeds" in parsed:
                            feeds = parsed.get("feeds", {})
                            if not feeds:
                                logger.warning(
                                    "⚠️ Received 'feeds' payload but it's empty."
                                )
                                continue
                            self.received_ltp = True
                            logger.info(
                                f"✅ Calling callback for {len(feeds)} batched LTPs."
                            )
                            await self.callback({"type": "live_feed", "data": feeds})
                            if self.market_closed:
                                logger.info(
                                    "📴 Market is closed & batched LTP received. Stopping."
                                )
                                self.should_run = False
                        else:
                            logger.warning(f"⚠️ Unknown message type: {msg_type}")

            except PermissionError:
                await self.callback({"type": "error", "reason": "token_expired"})
                self.should_run = False
                break

            except InvalidStatus as e:
                logger.error(f"❌ WebSocket rejected: {e}")
                if getattr(e, "status", None) == 403:
                    if self.on_auth_error and not self.auth_error_sent:
                        await self.on_auth_error()
                        self.auth_error_sent = True
                break

            except Exception as e:
                logger.error(f"🔥 Unexpected error: {e}")
                self.retry_count += 1
                await asyncio.sleep(3)

        await self._trigger_stop_callback()

    async def _send_subscription(self):
        if not self.websocket:
            return
        payload = {
            "guid": "algo-dashboard",
            "method": "sub",
            "data": {
                "mode": "full",
                "instrumentKeys": self.instrument_keys[:1500],
            },
        }
        await self.websocket.send(json.dumps(payload).encode("utf-8"))
        logger.info("📩 Subscription payload sent.")

    async def _trigger_stop_callback(self):
        if self.stop_callback:
            if inspect.iscoroutinefunction(self.stop_callback):
                await self.stop_callback()
            else:
                self.stop_callback()

    def stop(self):
        logger.info("🛑 WebSocket manually stopped.")
        self.should_run = False
