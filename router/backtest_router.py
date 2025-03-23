from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.connection import get_db
from services.backtest import backtest_ai_strategy

router = APIRouter(prefix="/api/backtest")

@router.get("/")
async def run_backtest(user_id: int, symbol: str, db: Session = Depends(get_db)):
    """Run AI backtesting on historical data."""
    return backtest_ai_strategy(user_id, symbol, db)
