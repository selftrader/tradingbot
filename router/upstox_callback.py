from fastapi import APIRouter, Request, Query
from broker.upstox_client import exchange_code_for_token_v2

router = APIRouter()

@router.get("/callback")
async def upstox_callback(request: Request, client_id: str = Query(...), client_secret: str = Query(...)):
    """
    Callback endpoint captures the authorization code along with client credentials from the UI.
    Example callback URL: http://yourdomain.com/callback?code=mk404x&client_id=...&client_secret=...
    """
    code = request.query_params.get("code")
    if not code:
        return {"error": "Missing code in callback"}
    
    access_token = exchange_code_for_token_v2(code, client_id, client_secret)
    return {"message": "Authentication successful", "access_token": access_token}