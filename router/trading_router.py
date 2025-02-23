from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.connection import get_db
from typing import List, Dict
from datetime import datetime

from database.models import Position, Trade

router = APIRouter(prefix="/api/trading", tags=["trading"])

@router.post("/order")
async def place_order(
    trade_request: Dict,
    db: Session = Depends(get_db)
):
    try:
        trade = Trade(
            symbol=trade_request['symbol'],
            trade_type=trade_request['trade_type'],
            quantity=trade_request['quantity'],
            price=trade_request.get('price'),
            stop_loss=trade_request.get('stop_loss'),
            target=trade_request.get('target'),
            status='PENDING',
            placed_at=datetime.utcnow()
        )
        db.add(trade)
        db.commit()
        db.refresh(trade)
        return {"message": "Order placed successfully", "trade_id": trade.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/positions")
async def get_positions(db: Session = Depends(get_db)):
    try:
        positions = db.query(Position).all()
        return positions
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))