from sqlalchemy.orm import Session
from database.models import AITradeJournal

def save_trade_to_journal(user_id: int, symbol: str, trade_type: str, ai_confidence: float, status: str, db: Session):
    """Save AI trade decisions to the journal for analysis."""
    
    trade_entry = AITradeJournal(
        user_id=user_id,
        symbol=symbol,
        trade_type=trade_type,
        ai_confidence=ai_confidence,
        execution_status=status
    )
    
    db.add(trade_entry)
    db.commit()
