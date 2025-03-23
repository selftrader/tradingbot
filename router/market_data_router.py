from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database.connection import get_db
from router.broker_router import get_current_user
from services.market_data_service import (
    fetch_live_stock_price,
    fetch_market_depth,
    fetch_holdings,
    fetch_positions,
    get_stock_snapshot  # ✅ Our fixed function
)

market_data_router = APIRouter(prefix="/api/market-data", tags=["Market Data"])


# ✅ 1. Live Price
@market_data_router.get("/live")
async def get_live_price(user_id: int, symbol: str, db: Session = Depends(get_db)):
    return fetch_live_stock_price(user_id, symbol, db)

# ✅ 2. Market Depth
@market_data_router.get("/depth")
async def get_market_depth(user_id: int, symbol: str, db: Session = Depends(get_db)):
    return fetch_market_depth(user_id, symbol, db)

# ✅ 4. Live Snapshot for Dashboard
@market_data_router.get("/stock/snapshot")
def get_market_snapshot(
    symbol: str,
    db: Session = Depends(get_db),
    current_user: int = Depends(get_current_user)
):
    return get_stock_snapshot(user_id=current_user, symbol=symbol, db=db)


