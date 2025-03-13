from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from database.connection import get_db
from database.models import Stock  # Ensure the Stock model is defined

stock_list_router = APIRouter()

@stock_list_router.get("/search", tags=["Stock Data"])
async def search_stocks(
    exchange: str = Query("NSE"),
    symbol: str = Query(None),  # Optional filtering by symbol
    name: str = Query(None),  # Optional filtering by stock name
    db: Session = Depends(get_db)
):
    """Fetch only the stocks that are added for trading execution."""
    query = db.query(Stock).filter(Stock.exchange == exchange)

    if symbol:
        query = query.filter(Stock.symbol.ilike(f"%{symbol}%"))  # Case-insensitive search
    if name:
        query = query.filter(Stock.name.ilike(f"%{name}%"))  # Case-insensitive search

    stocks = query.all()

    return stocks

