from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from services.auth_service import get_current_user
from services.upstox.feed_manager import upstox_feed_manager
import logging
import json
from database.connection import db
from database.models import BrokerConfig
from sqlalchemy.orm import Session

logger = logging.getLogger(__name__)

market_ws_router = APIRouter()


@market_ws_router.websocket("/ws/market")
async def market_data_websocket(websocket: WebSocket):
    await websocket.accept()
    logger.info("📥 WebSocket client connected")

    try:
        jwt_token = websocket.query_params.get("token")

        # Authenticate the user with that token
        user = get_current_user(jwt_token, db)

        # Get user's Upstox config
        broker = (
            db.query(BrokerConfig).filter_by(user_id=user.id, broker="upstox").first()
        )

        if not broker or not broker.access_token:
            await websocket.send_json({"error": "No Upstox token found"})
            return

        access_token = broker.access_token  # ✅ Use this to connect to Upstox Feed
        await upstox_feed_manager.initialize(access_token)

        while True:
            data = await websocket.receive_text()
            message = json.loads(data)

            if message.get("action") == "add_stock":
                instrument_key = message.get("instrumentKey")
                if instrument_key:
                    await upstox_feed_manager.subscribe_to_instrument(
                        instrument_key, websocket
                    )
                    await websocket.send_json(
                        {"status": "subscribed", "instrumentKey": instrument_key}
                    )
                    logger.info(f"✅ Subscribed: {instrument_key}")
                else:
                    await websocket.send_json({"error": "Missing instrumentKey"})

    except WebSocketDisconnect:
        logger.info("🔌 WebSocket disconnected")
    except Exception as e:
        logger.error(f"❌ WebSocket error: {e}")
        await websocket.close()
