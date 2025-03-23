from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.connection import get_db
from services.dynamic_stop_loss import calculate_dynamic_stop_loss

router = APIRouter(prefix="/api/stop_loss")

@router.post("/")
async def update_stop_loss(user_id: int, symbol: str, db: Session = Depends(get_db)):
    """Manually update AI-based stop-loss."""
    return calculate_dynamic_stop_loss(user_id, symbol, db)
