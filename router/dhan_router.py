from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from router.broker_router import get_current_user
from services.dhan_service import fetch_market_data, fetch_live_stock_price
from database.connection import get_db

dhan_router = APIRouter()

@dhan_router.get("/historical")
async def get_historical_data(
    user_id: int = Depends(get_current_user), 
    symbol: str = "RELIANCE",
    exchange: str = "NSE",
    instrument: str = "EQUITY",
    db: Session = Depends(get_db)
):
    """Fetch historical market data using Dhan API credentials stored in DB."""
    data = fetch_market_data(user_id, symbol, exchange, instrument, db)
    if "error" in data:
        raise HTTPException(status_code=500, detail=data["error"])
    return data

@dhan_router.get("/live/{symbol}")
async def get_live_stock_price(
    symbol: str,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Fetch real-time stock price using Dhan API credentials stored in DB."""
    price_data = fetch_live_stock_price(user_id, symbol, db)
    if "error" in price_data:
        raise HTTPException(status_code=500, detail=price_data["error"])
    return price_data
