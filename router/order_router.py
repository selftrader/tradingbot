from fastapi import APIRouter, HTTPException, Depends
from database.models import Order  # ✅ Import Order model
from database.connection import SessionLocal
import requests
import os

router = APIRouter()

BROKER_API_URL = os.getenv("BROKER_API_URL")  # ✅ Your broker API (like Zerodha, Upstox, etc.)

# ✅ Function to fetch broker details
def get_broker_details(user_id, db):
    return db.query(Order).filter(Order.user_id == user_id, Order.is_active == True).first()

@router.post("/trade/execute")
async def execute_trade(symbol: str, quantity: int, order_type: str, side: str, user_id: int):
    """
    Execute a trade order.
    - symbol: Stock symbol (e.g., "RELIANCE")
    - quantity: Number of shares
    - order_type: "market" or "limit"
    - side: "buy" or "sell"
    """

    db = SessionLocal()
    broker = get_broker_details(user_id, db)
    if not broker:
        raise HTTPException(status_code=400, detail="No active broker account found.")

    order_payload = {
        "symbol": symbol,
        "quantity": quantity,
        "order_type": order_type,
        "side": side,
        "api_key": broker.api_key,
        "api_secret": broker.api_secret
    }

    try:
        response = requests.post(f"{BROKER_API_URL}/place_order", json=order_payload)
        data = response.json()

        if response.status_code == 200:
            return {"status": "success", "order_id": data["order_id"], "message": "Trade executed successfully!"}
        else:
            raise HTTPException(status_code=400, detail=data["message"])
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
