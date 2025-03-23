from sqlalchemy.orm import Session
from database.models import HistoricalData
from services.dhan_client import get_dhan_client

def fetch_and_store_historical_data(user_id: int, symbol: str, from_date: str, to_date: str, db: Session):
    """Fetch historical market data from Dhan API and store in DB."""
    try:
        client = get_dhan_client(user_id, db)
        response = client.get_historical_data(symbol=symbol, exchange="NSE", from_date=from_date, to_date=to_date)
        
        for data in response.get("data", []):
            historical_entry = HistoricalData(
                user_id=user_id,
                symbol=symbol,
                exchange="NSE",
                date=data["date"],
                open=data["open"],
                high=data["high"],
                low=data["low"],
                close=data["close"],
                volume=data["volume"]
            )
            db.add(historical_entry)
        
        db.commit()
        return {"message": f"✅ Historical data for {symbol} stored successfully"}
    
    except Exception as e:
        return {"error": f"Failed to fetch historical data: {e}"}
