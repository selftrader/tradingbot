from sqlalchemy.orm import Session
from database.models import TradeSignal
from services.trade_execution import execute_trade_with_sizing

CONFIDENCE_THRESHOLD = 75  # ✅ AI must be at least 75% confident before executing

def auto_execute_trades(user_id: int, db: Session):
    """AI automatically executes high-confidence trade signals."""
    
    trade_signals = db.query(TradeSignal).filter(
        TradeSignal.user_id == user_id,
        TradeSignal.execution_status == "PENDING",
        TradeSignal.confidence >= CONFIDENCE_THRESHOLD
    ).all()

    for signal in trade_signals:
        result = execute_trade_with_sizing(user_id, signal.symbol, signal.trade_type, db)
        
        # ✅ Mark trade as EXECUTED
        signal.execution_status = "EXECUTED"
        db.commit()

    return {"message": f"✅ {len(trade_signals)} trades executed based on AI confidence"}
