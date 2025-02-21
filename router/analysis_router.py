from fastapi import APIRouter, Depends, HTTPException, Request
from typing import List, Optional
from datetime import datetime
from models.stock_selector import StockSelector
from config import SECTORAL_INDICES
from services.options_analyzer import OptionsAnalyzer
from sqlalchemy.orm import Session
from database.connection import get_db
from services.technical_analysis import TechnicalAnalysis
import yfinance as yf
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/analysis", tags=["analysis"])

# Create analyzers lazily when needed
_stock_selector = None
_options_analyzer = None

def get_stock_selector():
    global _stock_selector
    if (_stock_selector is None):
        _stock_selector = StockSelector()
    return _stock_selector

def get_options_analyzer():
    global _options_analyzer
    if (_options_analyzer is None):
        _options_analyzer = OptionsAnalyzer()
    return _options_analyzer

# Initialize technical analysis service
technical_analysis = TechnicalAnalysis()
ta_service = TechnicalAnalysis()

@router.get("/sector/{sector_name}/stocks")
async def analyze_sector_stocks(sector_name: str):
    """Analyze stocks for a specific sector"""
    try:
        if sector_name not in SECTORAL_INDICES:
            raise HTTPException(status_code=404, detail="Sector not found")

        logger.info(f"Starting analysis for sector: {sector_name}")
        
        # Get selector instance only when needed
        selector = get_stock_selector()
        symbols = SECTORAL_INDICES[sector_name]
        
        # Train model and analyze stocks
        try:
            selector.train_model(symbols)
            signals = selector.analyze_stocks(symbols, sector_name)
        except Exception as analysis_error:
            logger.error(f"Analysis failed: {str(analysis_error)}")
            raise HTTPException(
                status_code=500,
                detail="Failed to analyze stocks"
            )

        if not signals:
            return {
                "sector": sector_name,
                "analysis_time": datetime.now().isoformat(),
                "message": "No trading signals found",
                "recommendations": []
            }

        return {
            "sector": sector_name,
            "analysis_time": datetime.now().isoformat(),
            "recommendations": [
                {
                    "symbol": signal.symbol,
                    "action": signal.trade_type,
                    "entry": round(signal.entry_price, 2),
                    "target": round(signal.target_price, 2),
                    "stop_loss": round(signal.stop_loss, 2),
                    "confidence": f"{signal.confidence:.2%}",
                    "risk_reward": f"{signal.risk_reward:.2f}"
                }
                for signal in signals[:5]  # Top 5 recommendations
            ]
        }

    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Analysis failed: {str(e)}"
        )

@router.get("/analyze_sectoral_options")
async def analyze_sectoral_options():
    """Analyze options across all sectors and return trading opportunities"""
    try:
        all_recommendations = []
        # Get analyzer instance only when needed
        options_analyzer = get_options_analyzer()

        for sector_name, symbols in SECTORAL_INDICES.items():
            try:
                sector_analysis = await options_analyzer.analyze_sector_options(
                    sector=sector_name,
                    symbols=symbols
                )
                
                if sector_analysis and sector_analysis['recommendations']:
                    all_recommendations.extend([
                        {
                            **rec,
                            'sector': sector_name
                        } for rec in sector_analysis['recommendations']
                    ])
            except Exception as sector_error:
                print(f"Error analyzing {sector_name}: {str(sector_error)}")
                continue

        # Sort by confidence and limit to top opportunities
        sorted_recommendations = sorted(
            all_recommendations,
            key=lambda x: float(x['confidence'].rstrip('%')),
            reverse=True
        )[:10]  # Top 10 opportunities across sectors

        return {
            "analysis_time": datetime.now().isoformat(),
            "total_opportunities": len(sorted_recommendations),
            "recommendations": sorted_recommendations
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Sectoral options analysis failed: {str(e)}"
        )

@router.get("/stock/{symbol}")
async def analyze_stock(
    symbol: str,
    period: str = "1d",
    interval: str = "5m",
    db: Session = Depends(get_db)
):
    """Analyze a single stock"""
    try:
        logger.info(f"Analyzing stock: {symbol}")
        data = yf.download(symbol, period=period, interval=interval)
        
        if data.empty:
            raise HTTPException(
                status_code=404,
                detail=f"No data found for symbol: {symbol}"
            )
        
        analysis = ta_service.analyze_stock(data)
        
        return {
            "symbol": symbol,
            "timestamp": datetime.utcnow().isoformat(),
            "current_price": float(data['Close'].iloc[-1]),
            "analysis": analysis,
            "indicators": {
                "rsi": float(analysis.get('RSI', 0)),
                "macd": float(analysis.get('MACD', 0)),
                "signal": float(analysis.get('Signal', 0)),
                "trend": analysis.get('Trend', 'NEUTRAL')
            }
        }
    except Exception as e:
        logger.error(f"Analysis error for {symbol}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/market/scan")
async def scan_market(
    symbols: List[str] = None,
    db: Session = Depends(get_db)
):
    """Scan multiple stocks for trading opportunities"""
    if not symbols:
        symbols = ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS"]
    
    try:
        results = []
        for symbol in symbols:
            try:
                analysis = await analyze_stock(symbol, db=db)
                if analysis['indicators']['trend'] != 'NEUTRAL':
                    results.append(analysis)
            except Exception as e:
                logger.error(f"Error analyzing {symbol}: {str(e)}")
                continue
                
        return {
            "scan_time": datetime.utcnow().isoformat(),
            "results": results,
            "total_scanned": len(symbols),
            "opportunities_found": len(results)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/start")
async def start_analysis(request: Request, db: Session = Depends(get_db)):
    """Explicitly start stock analysis"""
    try:
        controller = request.app.state.trading_controller
        await controller.start_analysis()
        return {"message": "Analysis started successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/stop")
async def stop_analysis(request: Request):
    """Stop ongoing analysis"""
    try:
        controller = request.app.state.trading_controller
        await controller.stop_analysis()
        return {"message": "Analysis stopped successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))