from fastapi import Depends, WebSocket, WebSocketDisconnect, APIRouter
from sqlalchemy.orm import Session
from database.connection import get_db
from database.models import User
from services.auth_service import get_current_user
from services.upstox.ws_feed_v3 import UpstoxWebSocketClient
from services.upstox.ws_manager import UpstoxWebSocketManager
import asyncio
import logging

logger = logging.getLogger(__name__)
market_ws_router = APIRouter()
ws_manager = UpstoxWebSocketManager()

active_clients: dict[str, UpstoxWebSocketClient] = {}


@market_ws_router.websocket("/ws/market")
async def websocket_endpoint(websocket: WebSocket, db: Session = Depends(get_db)):
    await websocket.accept()
    logger.info("📥 New WebSocket connection")

    user = None
    instrument_keys = []

    try:
        token = websocket.query_params.get("token")
        if not token:
            await websocket.send_json({"error": "Missing access token"})
            await websocket.close()
            return

        user: User = get_current_user(token, db)
        if not user:
            await websocket.send_json({"error": "Invalid token"})
            await websocket.close()
            return

        upstox_config = next(
            (b for b in user.broker_configs if b.broker_name.lower() == "upstox"), None
        )
        if not upstox_config or not upstox_config.access_token:
            await websocket.send_json({"error": "Upstox not linked"})
            await websocket.close()
            return

        first_sub = await websocket.receive_json()
        instrument_keys = first_sub.get("data", {}).get("instrumentKeys", [])
        if not instrument_keys:
            await websocket.send_json({"error": "No instrument keys provided"})
            await websocket.close()
            return

        await ws_manager.connect(user.email, websocket, instrument_keys)

        if user.email not in active_clients:
            client = UpstoxWebSocketClient(ws_manager)
            active_clients[user.email] = client
            asyncio.create_task(
                client.start(user_email=user.email, instrument_keys=instrument_keys)
            )
            logger.info(f"✅ Upstox client started for user {user.email}")
        else:
            client = active_clients[user.email]
            new_keys = list(set(instrument_keys) - set(client.instrument_keys))
            if new_keys:
                await client.subscribe_to_new_instruments(new_keys)
                logger.info(f"🆕 Added new instruments for {user.email}: {new_keys}")

        await websocket.send_json(
            {"status": "connected", "message": "Market feed connected"}
        )

        async def subscription_listener():
            nonlocal instrument_keys
            try:
                while True:
                    message = await websocket.receive_json()
                    if "data" in message and "instrumentKeys" in message["data"]:
                        new_keys = message["data"]["instrumentKeys"]
                        current_keys_set = set(instrument_keys)
                        new_keys_set = set(new_keys)

                        if not new_keys_set.issubset(current_keys_set):
                            to_add = list(new_keys_set - current_keys_set)
                            instrument_keys = list(current_keys_set.union(new_keys_set))
                            if user.email in active_clients:
                                await active_clients[
                                    user.email
                                ].subscribe_to_new_instruments(to_add)
                                logger.info(f"➕ Subscribed new keys: {to_add}")
            except WebSocketDisconnect:
                logger.info("🔌 WebSocket closed in subscription listener")
            except Exception as e:
                logger.warning(f"⚠️ Error in dynamic subscription: {e}")

        async def ping_listener():
            try:
                while True:
                    text = await websocket.receive_text()
                    if text.strip().lower() == "ping":
                        await websocket.send_text("pong")
            except WebSocketDisconnect:
                logger.info("🔌 WebSocket closed in ping listener")
            except Exception as e:
                logger.warning(f"⚠️ Message loop error: {e}")

        await asyncio.gather(subscription_listener(), ping_listener())

    except WebSocketDisconnect:
        logger.info("🔌 WebSocket disconnected")
    except Exception as e:
        logger.error(f"❌ Unexpected WebSocket error: {str(e)}")
        try:
            await websocket.send_json({"error": str(e)})
        except:
            pass
    finally:
        if user:
            await ws_manager.disconnect(user.email, websocket)
            if (
                not ws_manager.has_active_connection(user.email)
                and user.email in active_clients
            ):
                active_clients[user.email].stop()
                del active_clients[user.email]
                logger.info(f"🧹 Cleaned up WebSocket client for {user.email}")


@market_ws_router.get("/market/connections")
async def get_connection_stats():
    return {
        "active_connections": ws_manager.get_active_connections_count(),
        "subscribed_instruments": ws_manager.get_subscribed_instruments_count(),
    }
