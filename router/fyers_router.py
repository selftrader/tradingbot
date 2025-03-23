from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel
from sqlalchemy.orm import Session
from uuid import UUID
from datetime import datetime

from database.connection import get_db
from database.models import BrokerConfig, User
from services.auth_service import get_current_user
from services.fyers_service import generate_fyers_auth_url, exchange_code_for_fyers_token
from services.fyers_temp_store import (
    store_fyers_credentials_temp,
    get_fyers_credentials_temp,
    clear_fyers_credentials_temp
)

fyers_router = APIRouter()

class FyersConfigRequest(BaseModel):
    broker: str  # "Fyers"
    config: dict  # client_id, secret_key, redirect_uri


@fyers_router.post("/init-auth")
def initiate_fyers_auth(data: FyersConfigRequest, user: User = Depends(get_current_user)):
    client_id = data.config.get("client_id")
    secret_key = data.config.get("secret_key")
    redirect_uri = data.config.get("redirect_uri")

    if not all([client_id, secret_key, redirect_uri]):
        raise HTTPException(status_code=400, detail="Missing Fyers credentials")

    state = str(user.id)
    store_fyers_credentials_temp(state, client_id, secret_key, redirect_uri)
    auth_url = generate_fyers_auth_url(client_id, secret_key, redirect_uri, state)

    return {"auth_url": auth_url}


@fyers_router.get("/callback")
def fyers_callback(
    s: str = Query(...),
    code: str = Query(...),
    auth_code: str = Query(...),
    state: str = Query(...),
    db: Session = Depends(get_db)
):
    try:
        
        if s != "ok":
            raise HTTPException(status_code=400, detail="Fyers auth failed")
        if code != "200":
            raise HTTPException(status_code=400, detail="Fyers auth failed")
       
        # Parse state (user_id)
        try:
            user_id = str(state)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid user ID in state")

        # Fetch user
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        # Get credentials from temporary store
        creds = get_fyers_credentials_temp(user_id)
        if not creds:
            raise HTTPException(status_code=400, detail="Missing temporary credentials")

        # Exchange the auth_code for token
        token_response = exchange_code_for_fyers_token(
            code=auth_code,
            client_id=creds["client_id"],
            secret_key=creds["secret_key"],
            redirect_uri=creds["redirect_uri"]
        )

        if "access_token" not in token_response:
            raise HTTPException(status_code=400, detail="Token exchange failed")

        if access_token := token_response.get("access_token"):
            isverified = True
        else:
            isverified = False
        # Store broker config
        broker_config = BrokerConfig(
            user_id=user_id,
            broker_name="fyers",
            api_key=creds["client_id"],
            api_secret=creds["secret_key"],
            access_token=token_response["access_token"],
            refresh_token=token_response.get("refresh_token"),
            created_at=datetime.utcnow(),
            config={},
            additional_params=token_response
        )

        db.add(broker_config)
        db.commit()

        clear_fyers_credentials_temp(user_id)

        return {"message": "Fyers broker linked successfully"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fyers callback error: {str(e)}")