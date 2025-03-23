import numpy as np
from sqlalchemy.orm import Session
from database.models import TradePerformance
from services.dhan_client import get_dhan_client

def update_trailing_stop_loss(user_id: int, symbol: str, db: Session):
    """AI dynamically adjusts trailing stop-loss based on price movement."""

    client = get_dhan_client(user_id, db)
    live_price = client.get_market_data(symbol, exchange="NSE")["ltp"]

    # Fetch open trade
    trade = db.query(TradePerformance).filter(
        TradePerformance.symbol == symbol, TradePerformance.status == "OPEN"
    ).first()

    if trade:
        new_stop_loss = trade.trailing_stop_loss  # Keep the last stop-loss

        if trade.trade_type == "BUY":
            if live_price > trade.trailing_stop_loss * 1.02:  # 2% move up
                new_stop_loss = live_price * 0.98  # Keep 2% below the highest price

        elif trade.trade_type == "SELL":
            if live_price < trade.trailing_stop_loss * 0.98:  # 2% move down
                new_stop_loss = live_price * 1.02  # Keep 2% above the lowest price

        if new_stop_loss != trade.trailing_stop_loss:
            trade.trailing_stop_loss = new_stop_loss
            db.commit()
            return {"message": f"✅ Trailing Stop-Loss updated: {symbol} at ₹{new_stop_loss}"}

    return {"message": "⚠️ No update required."}
