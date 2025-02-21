from fastapi import APIRouter, HTTPException
from pydantic import BaseModel


# Import Upstox client from our broker module
from upstox_api.api import Upstox
from broker.upstox_data_fetcher import UpstoxDataFetcher

# Import the configuration controller router and re-export it.
from controllers.configuration_controller import router as configuration_router

router = APIRouter()
router.include_router(configuration_router)

class BrokerConfiguration(BaseModel):
    broker: str
    config: dict

@router.post("/api/configuration")
async def save_configuration_endpoint(configuration: BrokerConfiguration):
    broker = configuration.broker
    config = configuration.config

    if not broker or not config:
        raise HTTPException(status_code=400, detail="Invalid payload")

    print(f"Received configuration for {broker}: {config}")
    login_url = None

    if broker.lower() in ["upstox", "upstocks"]:
        client_id = config.get("clientId")
        client_secret = config.get("clientSecret")
        redirect_uri = config.get("redirectUri")
        if not client_id or not client_secret or not redirect_uri:
            raise HTTPException(status_code=400, detail="Missing Upstox configuration details")
        try:
            fetcher = UpstoxDataFetcher(client_id, client_secret, redirect_uri)
            # For this implementation, we obtain the login URL from the Upstox client.
            login_url = fetcher.authenticate().get_login_url()  
            print("Upstox Login URL:", login_url)
            # Optionally, persist the configuration in your database.
            return {"message": "Configuration saved successfully", "login_url": login_url}
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Error configuring Upstox: {e}")

    return {"message": "Configuration saved successfully"}