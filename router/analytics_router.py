from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.connection import get_db
from services.trade_analytics import get_trade_performance

router = APIRouter(prefix="/api/analytics")

@router.get("/")
async def trade_dashboard(user_id: int, db: Session = Depends(get_db)):
    """Fetch trade performance for analytics dashboard."""
    return get_trade_performance(user_id, db)
