import asyncio
import websockets
import json
from sqlalchemy.orm import Session
from database.models import TradePerformance
from services.dhan_client import get_dhan_client

async def send_profit_updates(user_id: int, db: Session):
    """Send real-time profit/loss updates over WebSockets."""
    async with websockets.connect("ws://localhost:8000/ws/profit") as websocket:
        while True:
            trades = db.query(TradePerformance).filter(
                TradePerformance.user_id == user_id, TradePerformance.status == "OPEN"
            ).all()

            profit_updates = []
            for trade in trades:
                live_price = get_dhan_client(user_id, db).get_market_data(trade.symbol, exchange="NSE")["ltp"]
                profit_loss = (live_price - trade.entry_price) if trade.trade_type == "BUY" else (trade.entry_price - live_price)
                
                profit_updates.append({
                    "symbol": trade.symbol,
                    "trade_type": trade.trade_type,
                    "entry_price": trade.entry_price,
                    "current_price": live_price,
                    "profit_loss": profit_loss
                })

            await websocket.send(json.dumps(profit_updates))
            await asyncio.sleep(5)
