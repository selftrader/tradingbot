from sqlalchemy.orm import Session
from database.models import TradePerformance

def get_trade_performance(user_id: int, db: Session):
    """Fetch trade history and profit/loss for the analytics dashboard."""
    
    trades = db.query(TradePerformance).filter(TradePerformance.user_id == user_id).all()
    trade_data = []
    
    for trade in trades:
        trade_data.append({
            "symbol": trade.symbol,
            "trade_type": trade.trade_type,
            "entry_price": trade.entry_price,
            "exit_price": trade.exit_price if trade.exit_price else "Open Trade",
            "profit_loss": trade.profit_loss if trade.profit_loss else "Pending",
            "trade_time": trade.trade_time,
            "status": trade.status
        })
    
    return trade_data
