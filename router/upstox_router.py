from datetime import datetime, timedelta
import os
import logging
from sqlalchemy.orm import Session
from urllib.parse import urlencode
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.responses import RedirectResponse, JSONResponse, HTMLResponse
from pydantic import BaseModel
from typing import Dict, Optional
import requests
from database.connection import SessionLocal, get_db
from database.models import BrokerConfig, User
from services.auth_service import get_current_user
from services.upstox_service import exchange_code_for_token, generate_upstox_auth_url
from services.upstox_temp_store import (
    store_upstox_credentials_temp,
    get_upstox_credentials_temp,
    clear_upstox_credentials_temp,
)

logger = logging.getLogger(__name__)
db = SessionLocal()

# Initialize router without prefix
upstox_router = APIRouter()
UPSTOX_REDIRECT_URI = os.getenv("UPSTOX_REDIRECT_URI")


class UpstoxConfiguration(BaseModel):
    broker: str
    config: Dict[str, str]


# @upstox_router.get("/callback")  # Path matches the callback URL from Upstox
# async def upstox_callback(code: str = Query(...), state: Optional[str] = Query(None)):
#     """
#     Callback endpoint that receives the authorization code from Upstox
#     """
#     try:
#         # Get stored credentials
#         stored_creds = next(iter(credentials_store.values()), None)
#         if not stored_creds:
#             raise HTTPException(
#                 status_code=400,
#                 detail="No stored credentials found"
#             )


#         # Clear stored credentials
#         credentials_store.clear()


#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))


@upstox_router.get("/status")
async def check_status():
    """
    Check Upstox connection status
    """
    # TODO: Implement status check logic
    return {"status": "operational"}


@upstox_router.post("/init-auth")
def initiate_upstox_auth(data: dict, user_id: int = Depends(get_current_user)):
    client_id = data.get("api_key")
    api_secret = data.get("api_secret")
    if not client_id:
        raise HTTPException(status_code=400, detail="Missing api_key")
    state = str(user_id.id)
    store_upstox_credentials_temp(state, client_id, api_secret)
    auth_url = generate_upstox_auth_url(client_id, user_id.id)
    return {"auth_url": auth_url}


# OAuth Callback Endpoint
@upstox_router.get("/callback")
def upstox_callback(code: str, state: str = None, db: Session = Depends(get_db)):
    try:
        user_id = int(state)
        user = db.query(User).filter(User.id == state).first() if state else None

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # ✅ Get creds from Redis
        creds = get_upstox_credentials_temp(user_id)
        if not creds:
            logger.error(f"No creds found in Redis for user_id={user_id}")
            raise HTTPException(status_code=400, detail="Missing temporary credentials")

        logger.info(f"Retrieved creds for user_id={user_id}")

        # ✅ Exchange for access token
        tokenResponse = exchange_code_for_token(
            code, creds["client_id"], creds["client_secret"]
        )

        # ✅ Find user
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            logger.error(f"User with id {user_id} not found in DB.")
            raise HTTPException(status_code=404, detail="User not found")

        # ✅ Save broker config
        broker = BrokerConfig(
            user_id=user_id,
            client_id=tokenResponse["user_id"],
            broker_name=tokenResponse["broker"],
            api_key=creds["client_id"],
            api_secret=creds["client_secret"],
            access_token=tokenResponse["access_token"],
            created_at=datetime.now(),
            is_active=tokenResponse["is_active"],
            additional_params=tokenResponse,
            config={
                "email": tokenResponse.get("email"),
                "user_name": tokenResponse.get("user_name"),
                "user_type": tokenResponse.get("user_type"),
                "poa": tokenResponse.get("poa"),
                "ddpi": tokenResponse.get("ddpi"),
                "exchanges": tokenResponse.get("exchanges"),
                "products": tokenResponse.get("products"),
                "order_types": tokenResponse.get("order_types"),
                "extended_token": tokenResponse.get("extended_token"),
            },
        )
        db.add(broker)
        db.commit()

        clear_upstox_credentials_temp(user_id)

        logger.info(f"Upstox linked successfully for user_id={user_id}")
        return {"message": "Upstox broker linked successfully."}

    except Exception as e:
        logger.exception(f"Upstox callback failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
