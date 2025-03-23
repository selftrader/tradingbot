from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.connection import get_db
from services.trade_entry_ai import detect_trade_signal

router = APIRouter(prefix="/api/trade_signals")

@router.get("/")
async def get_trade_signals(user_id: int, symbol: str, db: Session = Depends(get_db)):
    """Fetch AI-generated trade signals."""
    return detect_trade_signal(user_id, symbol, db)
