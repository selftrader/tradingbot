from fastapi import APIRouter, Query, HTTPException
from fastapi.responses import RedirectResponse
from upstox_api.api import Upstox
from broker.upstox_client import authenticate_upstox_v2

router = APIRouter()

@router.get("/api/upstox/status")
def upstox_status():
    # Placeholder endpoint
    return {"status": "Upstox endpoint works"}

@router.get("/login")
async def upstox_login(client_id: str = Query(...)):
    """
    Redirects the user to the Upstox API v2 login URL.
    The client_id is provided by the UI.
    """
    login_url = authenticate_upstox_v2(client_id)
    return RedirectResponse(login_url)