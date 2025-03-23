from dhanhq import dhanhq
from sqlalchemy.orm import Session
from database.repositories.broker_repo import get_dhan_credentials

def get_dhan_client(user_id: int, db: Session):
    """Dynamically initialize DhanHQ client using stored credentials."""
    credentials = get_dhan_credentials(user_id, db)
    if not credentials:
        raise ValueError("❌ No Dhan API credentials found in DB.")
    
    return dhanhq.DhanHQ(
        api_key=credentials["api_key"],
        access_token=credentials["access_token"]
    )
