from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.connection import get_db
from services.strategy_service import StrategyService
from typing import List, Dict

router = APIRouter(prefix="/api/strategy", tags=["strategy"])

@router.get("/analyze/{symbol}")
async def analyze_stock(
    symbol: str,
    timeframe: str = "1d",
    db: Session = Depends(get_db)
):
    """Analyze a stock for trading signals"""
    try:
        strategy_service = StrategyService(db)
        analysis = await strategy_service.analyze_stock(symbol, timeframe)
        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/scan/market")
async def scan_market(
    sector: str = None,
    db: Session = Depends(get_db)
):
    """Scan market for trading opportunities"""
    try:
        strategy_service = StrategyService(db)
        stocks = ["RELIANCE.NS", "TCS.NS", "INFY.NS"]  # Add more stocks as needed
        
        results = []
        for symbol in stocks:
            analysis = await strategy_service.analyze_stock(symbol)
            if analysis['signal'] in ['BUY', 'SELL']:
                results.append(analysis)
                
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))