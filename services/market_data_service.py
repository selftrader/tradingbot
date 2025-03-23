import logging
import dhanhq
from sqlalchemy.orm import Session
from services.dhan_client import get_dhan_client


def fetch_live_stock_price(user_id: int, symbol: str, db: Session):
    """Fetch real-time stock price from Dhan API."""
    try:
        client = get_dhan_client(user_id, db)
        response = client.get_market_data(symbol=symbol, exchange="NSE")
        return {
            "symbol": symbol,
            "livePrice": response.get("ltp", 0),
            "high": response.get("high", 0),
            "low": response.get("low", 0),
            "open": response.get("open", 0),
            "close": response.get("close", 0),
            "volume": response.get("volume", 0)
        }
    except Exception as e:
        logging.error(f"Failed to fetch live stock price: {e}")
        return {"error": f"Failed to fetch live price: {e}"}


def fetch_market_depth(user_id: int, symbol: str, db: Session):
    """Fetch real-time market depth from Dhan API."""
    try:
        client = get_dhan_client(user_id, db)
        response = client.get_market_depth(symbol=symbol, exchange="NSE")
        return response
    except Exception as e:
        logging.error(f"Failed to fetch market depth: {e}")
        return {"error": f"Failed to fetch market depth: {e}"}


def fetch_holdings(user_id: int, db: Session):
    """Fetch user's holdings from Dhan API."""
    try:
        client = get_dhan_client(user_id, db)
        return client.get_holdings()
    except Exception as e:
        logging.error(f"Failed to fetch holdings: {e}")
        return {"error": f"Failed to fetch holdings: {e}"}


def fetch_positions(user_id: int, db: Session):
    """Fetch user's open positions from Dhan API."""
    try:
        client = get_dhan_client(user_id, db)
        return client.get_positions()
    except Exception as e:
        logging.error(f"Failed to fetch positions: {e}")
        return {"error": f"Failed to fetch positions: {e}"}


def fetch_market_data(user_id: int, security_id: int, db: Session):
    """Fetch historical daily data using Dhan SDK."""
    creds = get_dhan_client(user_id, db)
    if not creds:
        logging.error("Dhan credentials not found.")
        return {"error": "No credentials found"}

    dhan = dhanhq(creds["client_id"], creds["access_token"])

    try:
        data = dhan.historical_daily_data(
            security_id=security_id,
            exchange_segment="NSE_EQ",
            instrument_type="EQUITY",
            expiry_code=0,
            from_date="2024-01-01",
            to_date="2024-03-19"
        )
        logging.info(f"Historical data for {security_id} fetched.")
        return data
    except Exception as e:
        logging.error(f"Error fetching historical data: {e}")
        return {"error": str(e)}


def get_stock_snapshot(user_id: int, symbol: str, db: Session):
    """Fetch real-time stock snapshot for dashboard add."""
    try:
        client = get_dhan_client(user_id, db)
        response = client.get_market_data(symbol=symbol, exchange="NSE")

        return {
            "name": symbol,
            "symbol": symbol,
            "exchange": "NSE",
            "instrument": "EQUITY",
            "livePrice": response.get("ltp", 0),
            "high": response.get("high", 0),
            "low": response.get("low", 0),
            "open": response.get("open", 0),
            "close": response.get("close", 0),
            "volume": response.get("volume", 0),
            "target": 0,
            "stopLoss": 0,
            "amount": 0
        }
    except Exception as e:
        logging.error(f"Failed to fetch snapshot for {symbol}: {e}")
        return {"error": f"Failed to fetch snapshot: {e}"}
