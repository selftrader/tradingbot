from sqlalchemy.orm import Session
from database.models import TradeHistory
from services.ai_model import train_lstm_model

def retrain_ai_model(user_id: int, symbol: str, db: Session):
    """Retrain AI model after analyzing past trade performance."""
    
    # Fetch past trades
    past_trades = db.query(TradeHistory).filter(
        TradeHistory.symbol == symbol, TradeHistory.status == "CLOSED"
    ).all()
    
    if len(past_trades) < 5:  # Minimum trades needed for retraining
        return {"message": "⚠️ Not enough trade data for retraining"}
    
    # Train new AI model with recent data
    train_lstm_model(user_id, symbol, db)
    
    return {"message": "✅ AI model retrained successfully"}
