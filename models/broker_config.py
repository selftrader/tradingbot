from pydantic import BaseModel
from typing import Optional, Dict

class BrokerConfig(BaseModel):
    broker_name: str
    api_key: str
    api_secret: str
    additional_params: Optional[Dict] = {}
    is_active: bool = False