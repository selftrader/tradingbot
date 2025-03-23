from sqlalchemy.orm import Session
from database.models import BrokerConfig

def get_dhan_credentials(user_id: int, db: Session):
    """Fetch stored API credentials for Dhan Broker from the database."""
    credentials = (
        db.query(BrokerConfig)
        .filter(BrokerConfig.user_id == user_id, BrokerConfig.broker_name == "Dhan", BrokerConfig.is_active == True)
        .first()
    )
    
    if not credentials:
        return None

    return {
        "broker_name": credentials.broker_name,
        "client_id": credentials.client_id,
        "api_key": credentials.api_key,
        "access_token": credentials.access_token,
        "refresh_token": credentials.refresh_token,
        "access_token_expiry": credentials.access_token_expiry
    }
