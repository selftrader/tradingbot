from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from broker.upstox_client import authenticate_upstox_v2

router = APIRouter()

class BrokerConfiguration(BaseModel):
    broker: str
    config: dict

@router.post("/api/configuration")
async def save_configuration(configuration: BrokerConfiguration):
    broker = configuration.broker
    config = configuration.config

    if not broker or not config:
        raise HTTPException(status_code=400, detail="Invalid payload")

    print(f"Saving configuration for {broker}: {config}")

    if broker.lower() in ['upstox', 'upstocks']:
        # With API v2, you may not need to pass client credentials via the payload.
        # Instead, use the configuration in your config.py
        login_url, access_token = authenticate_upstox_v2(config.get("clientId"))
        print("Upstox API v2 configuration processed successfully!")
        return {
            "message": "Configuration saved successfully",
            "login_url": login_url,
            "access_token": access_token
        }

    return {"message": "Configuration saved successfully"}