# routers/backtesting_router.py

from fastapi import APIRouter, Depends, Query, HTTPException
import httpx
from database.connection import get_db
from sqlalchemy.orm import Session
from database.models import BrokerConfig
from services.auth_service import get_current_user

backtesting_router = APIRouter()

@backtesting_router.get("/intraday-candles", tags=["Backtesting"])
async def get_intraday_candles(
    instrument_key: str = Query(...),
    interval: str = Query("1minute"),  # allowed: 1minute, 30minute
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    # 1. Get Upstox token from DB
    broker_config = db.query(BrokerConfig).filter_by(user_id=current_user["id"], broker="upstox").first()
    if not broker_config or not broker_config.access_token:
        raise HTTPException(status_code=400, detail="Upstox not configured for user.")

    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {broker_config.access_token}",
    }

    upstox_url = f"https://api.upstox.com/v2/historical-candle/intraday/{instrument_key}/{interval}"

    async with httpx.AsyncClient() as client:
        res = await client.get(upstox_url, headers=headers)

    if res.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to fetch candles from Upstox")

    data = res.json()
    return data["data"]
