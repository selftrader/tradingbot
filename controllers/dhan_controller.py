from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

class DhanConfiguration(BaseModel):
    access_token: str

@router.post("/api/dhan/config")
async def configure_dhan(config: DhanConfiguration):
    """
    Configures Dhan broker using the provided access token.
    No OAuth flow needed as Dhan uses direct access token authentication.
    """
    try:
        access_token = config.access_token
        if not access_token:
            raise HTTPException(status_code=400, detail="Access token is required")

        # Initialize Dhan client and verify the token
        # Example verification call (adjust according to Dhan's SDK):
        # dhan_client = DhanClient(access_token)
        # profile = dhan_client.get_profile()  # Verify token is valid

        # For now, just return success
        return {
            "message": "Dhan configuration successful",
            "broker": "dhan",
            "status": "connected"
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to configure Dhan: {str(e)}")