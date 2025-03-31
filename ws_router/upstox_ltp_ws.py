from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import json
from jose import jwt
from core.config import JWT_SECRET
from database.connection import SessionLocal
from database.models import User, BrokerConfig

from ws_clients.upstox_ws_client import UpstoxWebSocketClient

ws_upstox_router = APIRouter()
ALGORITHM = "HS256"

def get_access_token_from_token(token: str):
    payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
    email = payload.get("sub")
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        broker = db.query(BrokerConfig).filter(
            BrokerConfig.user_id == user.id,
            BrokerConfig.broker_name.ilike("upstox")
        ).first()
        return broker.access_token
    finally:
        db.close()

@ws_upstox_router.websocket("/ws/upstox/ltp")
async def ltp_ws(websocket: WebSocket):
    await websocket.accept()
    try:
        token = websocket.query_params.get("token")
        access_token = get_access_token_from_token(token)

        message = await websocket.receive_text()
        payload = json.loads(message)
        symbols = payload.get("symbols", [])

        if not symbols:
            await websocket.send_text(json.dumps({"error": "No symbols provided"}))
            return

        async def send_to_frontend(data):
            await websocket.send_text(json.dumps(data))

        # Start Upstox WebSocket
        client = UpstoxWebSocketClient(
            token=access_token,
            instruments=symbols,
            on_message=send_to_frontend
        )
        await client.connect()

    except WebSocketDisconnect:
        print("🔌 Client disconnected")
    except Exception as e:
        await websocket.send_text(json.dumps({"error": str(e)}))
    finally:
        await websocket.close()
