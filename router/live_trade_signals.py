import asyncio
from database.connection import SessionLocal
import websockets
import json
from sqlalchemy.orm import Session
from database.models import TradeSignal

async def send_trade_signals(user_id: int):
    """Send AI trade signals over WebSockets."""
    
    async with websockets.connect("ws://localhost:8000/ws/trade_signals") as websocket:
        while True:
            db = SessionLocal()
            signals = db.query(TradeSignal).filter(
                TradeSignal.user_id == user_id, TradeSignal.status == "PENDING"
            ).all()
            db.close()

            trade_signals = []
            for signal in signals:
                trade_signals.append({
                    "symbol": signal.symbol,
                    "trade_type": signal.trade_type,
                    "confidence": signal.confidence,
                    "status": signal.status
                })

            await websocket.send(json.dumps(trade_signals))
            await asyncio.sleep(5)
