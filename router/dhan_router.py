from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Dict, Optional
from broker.dhan_client import DhanClient

router = APIRouter()

class DhanConfiguration(BaseModel):
    broker: str
    config: Dict[str, str]

# Store credentials temporarily (use secure storage in production)
credentials_store: Dict[str, Dict[str, str]] = {}

@router.post("/api/dhan/configuration")
async def save_configuration(configuration: DhanConfiguration):
    try:
        client_id = configuration.config.get("clientId")
        if not client_id:
            raise HTTPException(status_code=400, detail="Missing client ID")

        # Store credentials
        credentials_store[client_id] = configuration.config

        # Initialize client and get login URL
        client = DhanClient(client_id=client_id, access_token="")
        result = await client.authenticate()
        
        return JSONResponse(result)

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process configuration: {str(e)}"
        )

@router.get("/auth/dhan/callback")
async def dhan_callback(
    request_token: str = Query(...),
    client_id: str = Query(...)
):
    try:
        stored_config = credentials_store.get(client_id)
        if not stored_config:
            raise HTTPException(
                status_code=400,
                detail="No stored credentials found"
            )

        client = DhanClient(
            client_id=client_id,
            access_token=""
        )
        
        access_token = await client.exchange_token(request_token)
        
        # Clear stored credentials
        credentials_store.pop(client_id, None)
        
        return JSONResponse({
            "message": "Authentication successful",
            "access_token": access_token
        })

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Callback processing failed: {str(e)}"
        )
