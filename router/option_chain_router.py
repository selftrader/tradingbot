# routers/option_chain_router.py
from fastapi import APIRouter, HTTPException
from services.dhan_service import fetch_option_chain

router = APIRouter(prefix="/api/option-chain", tags=["Option Chain"])

@router.get("/{security_id}")
async def get_option_chain(security_id: int):
    """
    API route to get option chain data for a specific security ID.
    """
    data = fetch_option_chain(security_id)
    if "error" in data:
        raise HTTPException(status_code=400, detail=data["error"])

    return data
