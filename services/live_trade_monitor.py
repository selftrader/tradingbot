import asyncio
from database.connection import SessionLocal
import websockets
import json
from sqlalchemy.orm import Session
from database.models import TradePerformance
from services.dhan_client import get_dhan_client

async def send_live_trade_updates(user_id: int):
    """Send live trade updates over WebSockets."""
    async with websockets.connect("ws://localhost:8000/ws/live_trades") as websocket:
        while True:
            db = SessionLocal()
            trades = db.query(TradePerformance).filter(TradePerformance.user_id == user_id, TradePerformance.status == "OPEN").all()
            db.close()

            trade_updates = []
            for trade in trades:
                live_price = get_dhan_client(user_id, db).get_market_data(trade.symbol, exchange="NSE")["ltp"]
                trade_updates.append({
                    "symbol": trade.symbol,
                    "trade_type": trade.trade_type,
                    "entry_price": trade.entry_price,
                    "current_price": live_price,
                    "trailing_stop_loss": trade.trailing_stop_loss
                })

            await websocket.send(json.dumps(trade_updates))
            await asyncio.sleep(5)
