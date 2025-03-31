from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from database.connection import get_db
from database.models import BrokerInstrument, Stock  # Ensure the Stock model is defined

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

@stock_list_router.get("/resolve", tags=["Stock Data"])
def resolve_full_stock_details(
    symbol: str = Query(...),
    exchange: str = Query(...),
    db: Session = Depends(get_db)
):
    """
    After selecting a stock, fetch full details by joining with broker_instruments.
    """

    stock = db.query(Stock).filter(Stock.symbol == symbol, Stock.exchange == exchange).first()
    if not stock:
        raise HTTPException(status_code=404, detail="Stock not found")

    instrument = (
        db.query(BrokerInstrument)
        .filter(BrokerInstrument.symbol == symbol, BrokerInstrument.exchange == exchange)
        .first()
    )

    if not instrument:
        raise HTTPException(status_code=404, detail="Instrument details not found")

    return {
        "id": f"{exchange}_{symbol}",
        "symbol": stock.symbol,
        "name": stock.name,
        "exchange": stock.exchange,
        "instrument": instrument.isin or instrument.instrument_key,
        "instrumentKey": instrument.instrument_key,
        "instrument_type": instrument.instrument_type,
        "segment": instrument.segment,
        "tick_size": instrument.tick_size,
        "lot_size": instrument.lot_size,
    }