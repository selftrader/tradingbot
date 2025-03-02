from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from database.models import BrokerConfig
from services.broker_factory import BrokerFactory

def place_order(user_id: int, broker_name: str, symbol: str, quantity: int, side: str, order_type: str, db: Session = Depends()):
    """Execute a trade with the selected broker"""
    broker_config = db.query(BrokerConfig).filter(
        BrokerConfig.user_id == user_id, BrokerConfig.broker_name == broker_name, BrokerConfig.is_active == True
    ).first()

    if not broker_config:
        raise HTTPException(status_code=400, detail="Broker configuration not found")

    broker = BrokerFactory.get_broker(broker_name, {"api_key": broker_config.api_key, "api_secret": broker_config.api_secret})
    
    return broker.place_order(symbol, quantity, side, order_type)
