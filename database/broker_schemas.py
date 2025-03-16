from pydantic import BaseModel
from typing import Optional

# ✅ Base Schema for All Brokers
class BrokerConfigSchema(BaseModel):
    broker_name: str
    api_key: str
    api_secret: str
    is_active: Optional[bool] = True  # ✅ Default: Active

    class Config:
        orm_mode = True  # ✅ Ensures compatibility with SQLAlchemy

# ✅ Zerodha Broker Schema
class ZerodhaBrokerSchema(BrokerConfigSchema):
    access_token: str
    client_id: str
    refresh_token: Optional[str] = None  # ✅ Optional refresh token

# ✅ Upstox Broker Schema
class UpstoxBrokerSchema(BrokerConfigSchema):
    access_token: str
    client_id: str
    refresh_token: Optional[str] = None  # ✅ Optional refresh token

# ✅ Dhan Broker Schema
class DhanBrokerSchema(BrokerConfigSchema):
    access_token: str
    client_id: str
    refresh_token: Optional[str] = None  # ✅ Optional refresh token

# ✅ Angel Broking Schema
class AngelBrokerSchema(BrokerConfigSchema):
    access_token: str
    client_id: str
    refresh_token: Optional[str] = None  # ✅ Optional refresh token
    
# ✅ Request Model for Adding Broker
class BrokerConfigRequest(BaseModel):
    broker_name: str
    api_key: str
    api_secret: str
