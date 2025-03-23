import asyncio
import websockets
import json
from services.ai_strategy import detect_trend_reversal
from database.connection import SessionLocal

async def send_ai_decision_updates(user_id: int):
    """Send real-time AI trade decisions over WebSockets."""
    async with websockets.connect("ws://localhost:8000/ws/ai_decisions") as websocket:
        while True:
            db = SessionLocal()
            trend_analysis = detect_trend_reversal(user_id, "RELIANCE", db)
            db.close()

            decision = {
                "symbol": "RELIANCE",
                "ai_status": trend_analysis["status"]
            }
            await websocket.send(json.dumps(decision))
            await asyncio.sleep(5)
