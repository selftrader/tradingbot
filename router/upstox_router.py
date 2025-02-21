from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.responses import RedirectResponse, JSONResponse, HTMLResponse
from pydantic import BaseModel
from typing import Dict, Optional
import requests
from broker.upstox_client import authenticate_upstox_v2, exchange_code_for_token_v2
from config import UPSTOX_REDIRECT_URI  # Import the redirect URI

# Initialize router without prefix
router = APIRouter()

class UpstoxConfiguration(BaseModel):
    broker: str
    config: Dict[str, str]

# Temporary storage for demo purposes
credentials_store: Dict[str, Dict[str, str]] = {}

@router.post("/api/upstox/configuration")  # Full path here
async def save_configuration(configuration: UpstoxConfiguration):
    """
    Initial endpoint that saves credentials and redirects to Upstox login
    """
    try:
        client_id = configuration.config.get("clientId")
        client_secret = configuration.config.get("clientSecret")

        if not client_id or not client_secret:
            raise HTTPException(status_code=400, detail="Missing credentials")

        # Store credentials temporarily
        credentials_store[client_id] = {
            "client_id": client_id,
            "client_secret": client_secret
        }

        # Get login URL
        result = authenticate_upstox_v2(
            client_id=client_id,
            redirect_uri=f"{UPSTOX_REDIRECT_URI}"
        )
        
        return JSONResponse(result)

    except Exception as e:
        print(f"Error in configuration: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process configuration: {str(e)}"
        )

@router.get("/auth/upstox/callback")  # Path matches the callback URL from Upstox
async def upstox_callback(code: str = Query(...), state: Optional[str] = Query(None)):
    """
    Callback endpoint that receives the authorization code from Upstox
    """
    try:
        # Get stored credentials
        stored_creds = next(iter(credentials_store.values()), None)
        if not stored_creds:
            raise HTTPException(
                status_code=400,
                detail="No stored credentials found"
            )

        # Exchange code for token
        access_token = exchange_code_for_token_v2(
            authorization_code=code,
            client_id=stored_creds["client_id"],
            client_secret=stored_creds["client_secret"],
            redirect_uri=UPSTOX_REDIRECT_URI
        )

        # Clear stored credentials
        credentials_store.clear()

        return {
            "message": "Authentication successful",
            "access_token": access_token
        }

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/status")
async def check_status():
    """
    Check Upstox connection status
    """
    # TODO: Implement status check logic
    return {"status": "operational"}

@router.get("/login")
async def redirect_to_login(client_id: str):
    """
    Endpoint that performs the actual redirect to Upstox login page
    """
    try:
        login_url = authenticate_upstox_v2(client_id)
        return RedirectResponse(url=login_url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))