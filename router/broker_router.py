from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.connection import get_db
from models.database_models import BrokerConfig
from typing import Dict
import logging
from services.broker_factory import BrokerFactory

router = APIRouter(prefix="/api/broker", tags=["broker"])
logger = logging.getLogger(__name__)

@router.post("/connect")
async def connect_broker(
    broker_data: Dict,
    db: Session = Depends(get_db)
):
    try:
        broker = BrokerConfig(
            broker_name=broker_data['broker_name'],
            api_key=broker_data['api_key'],
            api_secret=broker_data['api_secret'],
            config_data=broker_data.get('config_data', {})
        )
        db.add(broker)
        db.commit()
        db.refresh(broker)
        return {"message": "Broker connected successfully", "broker_id": broker.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/authenticate/{broker_name}")
async def authenticate_broker(broker_name: str, config: Dict):
    """Start broker authentication"""
    try:
        broker = BrokerFactory.get_broker(broker_name, config)
        result = await broker.authenticate()
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/callback/{broker_name}")
async def broker_callback(broker_name: str, token: str, config: Dict):
    """Handle broker authentication callback"""
    try:
        broker = BrokerFactory.get_broker(broker_name, config)
        access_token = await broker.generate_token(token)
        return {"status": "success", "access_token": access_token}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))