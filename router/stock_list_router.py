


from fastapi import APIRouter, Depends
from requests import Session

from database.connection import get_db


router = APIRouter()


@router.get("api/stocks/available")
async def get_available_stocks(db: Session = Depends(get_db)):
    """Get list of available stocks"""
    # For demonstration, return a static list. In practice, fetch from a DB or third-party service.
     
    stocks = [
        {"symbol": "NIFTY", "name": "Nifty 50", "sector": "NIFTY50"},
        {"symbol": "BANKNIFTY", "name": "Bank Nifty", "sector": "BANKNIFTY"},
        {"symbol": "RELIANCE", "name": "Reliance Industries", "sector": "NIFTY50"},
        {"symbol": "TCS", "name": "Tata Consultancy Services", "sector": "IT"}
    ]

    return stocks