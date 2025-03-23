from fastapi import APIRouter, Depends
from services.trade_service import execute_trade

router = APIRouter()

@router.post("/execute-trade/{order_id}")
async def execute_trade_api(order_id: int):
    """
    Executes a trade and broadcasts the update via WebSocket.
    """
    trade_result = await execute_trade(order_id)
    return {"message": "Trade executed", "trade": trade_result}
