from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.connection import get_db
from database.models import BrokerConfig
from pydantic import BaseModel
import os
import jwt
import requests


SECRET_KEY = os.getenv("JWT_SECRET", "mysecretkey")

broker_router = APIRouter()

# Request model for adding broker API key
class BrokerConfigRequest(BaseModel):
    broker_name: str
    api_key: str
    secret_key: str

# Add broker API key
@broker_router.post("/add_broker")
def add_broker(config: BrokerConfigRequest, token: str, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username = payload.get("sub")
    except:
        raise HTTPException(status_code=401, detail="Invalid token")

    new_config = BrokerConfig(user_id=username, broker_name=config.broker_name, config={"api_key": config.api_key, "secret_key": config.secret_key})
    db.add(new_config)
    db.commit()
    return {"message": f"{config.broker_name} added successfully"}


# Fetch user profile from broker API
@broker_router.get("/get_broker_profile")
def get_broker_profile(token: str, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username = payload.get("sub")
    except:
        raise HTTPException(status_code=401, detail="Invalid token")

    user_broker = db.query(BrokerConfig).filter(BrokerConfig.user_id == username).first()
    if not user_broker:
        raise HTTPException(status_code=400, detail="Broker not configured")

    broker_api_url = "https://api.broker.com/user/profile"
    headers = {"Authorization": f"Bearer {user_broker.config['api_key']}"}
    
    response = requests.get(broker_api_url, headers=headers)
    return response.json()
