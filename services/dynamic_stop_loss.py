import numpy as np
from sqlalchemy.orm import Session
from database.models import TradePerformance
from services.dhan_client import get_dhan_client

def calculate_dynamic_stop_loss(user_id: int, symbol: str, db: Session):
    """Dynamically adjust stop-loss based on market volatility."""

    # Fetch last 10-minute price movements
    client = get_dhan_client(user_id, db)
    historical_prices = client.get_historical_data(symbol, exchange="NSE", from_date="2023-01-01", to_date="2023-01-02")["data"]

    # Calculate volatility (standard deviation of price changes)
    price_changes = np.diff([data["close"] for data in historical_prices])
    volatility = np.std(price_changes)

    # Fetch open trade
    trade = db.query(TradePerformance).filter(
        TradePerformance.symbol == symbol, TradePerformance.status == "OPEN"
    ).first()

    if trade:
        # Adjust stop-loss based on volatility
        stop_loss = trade.entry_price - (volatility * 2) if trade.trade_type == "BUY" else trade.entry_price + (volatility * 2)
        
        # Update stop-loss in DB
        trade.stop_loss = stop_loss
        db.commit()

        return {"message": f"✅ Stop-loss updated for {symbol} at ₹{stop_loss}"}

    return {"message": "⚠️ No open trades found."}
