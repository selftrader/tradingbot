import requests
import logging
from sqlalchemy.orm import Session
from database.repositories.broker_repo import get_dhan_credentials

DHAN_API_BASE_URL = "https://api.dhan.co/v2"  # ✅ Updated to Dhan API v2

def fetch_market_data(user_id: int, symbol: str, exchange: str, instrument: str, db: Session):
    """Fetch historical market data from Dhan using stored credentials."""

    credentials = get_dhan_credentials(user_id, db)
    if not credentials:
        logging.error("❌ No Dhan API credentials found in DB.")
        return {"error": "Dhan API credentials not found"}

    headers = {
        "Authorization": f"Bearer {credentials['access_token']}",  # ✅ Use DB credentials
        "Content-Type": "application/json",
        "X-Dhan-Api-Key": credentials['api_key']
    }

    params = {
        "symbol": symbol,
        "exchange": exchange,
        "instrument": instrument
    }

    try:
        response = requests.get(f"{DHAN_API_BASE_URL}/market/historical", headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        
        logging.info(f"📊 Market Data for {symbol} fetched: {data}")
        return data
    except requests.RequestException as e:
        logging.error(f"❌ Failed to fetch market data: {e}")
        return {"error": "Failed to fetch market data"}

def fetch_live_stock_price(user_id: int, symbol: str, db: Session):
    """Fetch real-time stock price from Dhan using stored credentials."""
    
    credentials = get_dhan_credentials(user_id, db)
    if not credentials:
        logging.error("❌ No Dhan API credentials found in DB.")
        return {"error": "Dhan API credentials not found"}

    headers = {
        "Authorization": f"Bearer {credentials['access_token']}",
        "Content-Type": "application/json",
        "X-Dhan-Api-Key": credentials['api_key']
    }

    try:
        response = requests.get(f"{DHAN_API_BASE_URL}/market/live/{symbol}", headers=headers)
        response.raise_for_status()
        data = response.json()

        price = data.get("price", 0)
        logging.info(f"📈 Live Price for {symbol}: ₹{price}")
        return {"price": float(price)}
    except requests.RequestException as e:
        logging.error(f"❌ Failed to fetch live stock price: {e}")
        return {"error": "Failed to fetch live stock price"}


def fetch_option_chain(user_id: int, symbol: str, exchange: str, instrument: str, db: Session,security_id):
    """
    Fetch option chain data from Dhan API for a given security_id.
    """
    credentials = get_dhan_credentials(user_id, db)
    try:
        option_chain_data = credentials.option_chain(security_id=security_id)
        if not option_chain_data:
            logging.warning("⚠️ No option chain data received")
            return {"error": "No option chain data found"}

        return option_chain_data
    except Exception as e:
        logging.error(f"❌ Error fetching option chain: {e}")
        return {"error": "Failed to fetch option chain"}