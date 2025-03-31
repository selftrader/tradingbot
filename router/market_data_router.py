from fastapi import APIRouter, Depends, Query
from database.models import User
from brokers.dhan_broker import DhanBroker
from brokers.upstox_broker import UpstoxBroker
from services.auth_service import get_current_user

market_data_router = APIRouter(prefix="/api/market-data", tags=["Market Data"])

@market_data_router.get("/live")
def get_live_data(
    symbol: str = Query(...), 
    broker: str = Query(...),
    current_user: User = Depends(get_current_user)
):
    if broker == "dhan":
        broker_client = DhanBroker(
            current_user.broker_config.dhan_client_id,
            current_user.broker_config.dhan_token
        )
        return broker_client.get_market_data(symbol)

    elif broker == "upstox":
        broker_client = UpstoxBroker(current_user.broker_config.upstox_token)
        return broker_client.get_market_data(symbol)

    return {"error": "Broker not supported"}


@market_data_router.get("/historical")
def get_historical_data(
    symbol: str = Query(...),
    interval: str = Query(...),
    from_date: str = Query(...),
    to_date: str = Query(...),
    broker: str = Query(...),
    current_user: User = Depends(get_current_user)
):
    if broker == "dhan":
        broker_client = DhanBroker(
            current_user.broker_config.dhan_client_id,
            current_user.broker_config.dhan_token
        )
        return broker_client.get_historical_data(symbol, interval, from_date, to_date)

    elif broker == "upstox":
        broker_client = UpstoxBroker(current_user.broker_config.upstox_token)
        return broker_client.get_historical_data(symbol, interval, from_date, to_date)

    return {"error": "Broker not supported"}
