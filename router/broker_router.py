from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.connection import get_db
from database.models import BrokerConfig
from pydantic import BaseModel
import jwt
import os

SECRET_KEY = os.getenv("JWT_SECRET", "mysecretkey")
broker_router = APIRouter()

class BrokerConfigRequest(BaseModel):
    broker_name: str
    api_key: str
    secret_key: str

@broker_router.post("/add_broker")
def add_broker(config: BrokerConfigRequest, token: str, db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("sub")
    except:
        raise HTTPException(status_code=401, detail="Invalid token")

    new_config = BrokerConfig(
        user_id=user_id,
        broker_name=config.broker_name,
        api_key=config.api_key,
        api_secret=config.secret_key,
        is_active=True
    )
    db.add(new_config)
    db.commit()
    return {"message": f"{config.broker_name} added successfully"}

@broker_router.get("/get_brokers")
def get_brokers(token: str, db: Session = Depends(get_db)):
    """Fetch all brokers added by a user"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user_id = payload.get("sub")
    except:
        raise HTTPException(status_code=401, detail="Invalid token")

    brokers = db.query(BrokerConfig).filter(BrokerConfig.user_id == user_id).all()
    return {"brokers": brokers}
