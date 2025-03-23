from sqlalchemy.orm import Session
from database.models import UserCapital
from services.dhan_client import get_dhan_client

def calculate_trade_size(user_id: int, symbol: str, db: Session):
    """AI determines trade size based on user capital & risk level."""
    
    # Fetch user capital & risk percentage
    user_capital = db.query(UserCapital).filter(UserCapital.user_id == user_id).first()
    if not user_capital:
        return {"error": "User capital not found"}

    # Get live stock price
    live_price = get_dhan_client(user_id, db).get_market_data(symbol, exchange="NSE")["ltp"]

    # Calculate trade size
    risk_per_trade = (user_capital.total_capital * user_capital.risk_percentage) / 100
    trade_size = risk_per_trade / live_price

    return {"symbol": symbol, "trade_size": int(trade_size), "capital_used": risk_per_trade}
