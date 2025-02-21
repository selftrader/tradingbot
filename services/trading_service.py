# services/trading_service.py

import logging
import pandas as pd
from upstox_api.api import OHLCInterval
from broker.upstox_data_fetcher import UpstoxDataFetcher
from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from models.database_models import Trade, Position, User
from database.connection import get_db
from datetime import datetime
from .technical_analysis import TechnicalAnalysis
import yfinance as yf

logger = logging.getLogger(__name__)

class TradingService:
    """
    Provides business logic for the trading operations.
    """
    def __init__(self, api_key: str = None, api_secret: str = None, redirect_uri: str = None, db: Session = Depends(get_db)) -> None:
        if api_key and api_secret and redirect_uri:
            self.fetcher = UpstoxDataFetcher(api_key, api_secret, redirect_uri)
        self.db = db
        self.ta = TechnicalAnalysis()

    def run(self, symbol: str, start_date: str, end_date: str, interval: OHLCInterval) -> pd.DataFrame:
        """
        Executes the workflow: authenticate, fetch historical data, compute indicators,
        and save the processed data.
        """
        self.fetcher.authenticate()
        df = self.fetcher.fetch_historical_data(symbol, start_date, end_date, interval)
        df = self.fetcher.compute_indicators(df)
        self.fetcher.save_data(df, symbol)
        logger.info("Trading service execution complete.")
        return df

    async def place_trade(self, trade_data: dict, user_id: int):
        try:
            trade = Trade(
                user_id=user_id,
                symbol=trade_data['symbol'],
                trade_type=trade_data['trade_type'],
                quantity=trade_data['quantity'],
                price=trade_data.get('price'),
                stop_loss=trade_data.get('stop_loss'),
                target=trade_data.get('target'),
                status='PENDING'
            )
            self.db.add(trade)
            self.db.commit()
            return trade
        except Exception as e:
            self.db.rollback()
            raise HTTPException(status_code=500, detail=str(e))

    async def analyze_stock(self, symbol: str):
        try:
            # Download data
            data = yf.download(symbol, period="1y", interval="1d")
            
            # Calculate indicators
            data = self.ta.calculate_indicators(data)
            
            # Generate signals
            signals = self._generate_signals(data)
            
            return {
                "symbol": symbol,
                "current_price": data['Close'][-1],
                "signals": signals,
                "indicators": {
                    "rsi": data.get('RSI_14', pd.Series())[-1],
                    "macd": data.get('MACD', pd.Series())[-1],
                    "signal": data.get('Signal', pd.Series())[-1]
                }
            }
        except Exception as e:
            logger.error(f"Error analyzing {symbol}: {str(e)}")
            raise

    def _generate_signals(self, data):
        """Generate trading signals based on technical indicators"""
        signals = []
        
        # RSI signals
        if 'RSI_14' in data.columns:
            last_rsi = data['RSI_14'].iloc[-1]
            if last_rsi < 30:
                signals.append({"indicator": "RSI", "signal": "BUY", "value": last_rsi})
            elif last_rsi > 70:
                signals.append({"indicator": "RSI", "signal": "SELL", "value": last_rsi})

        # MACD signals
        if all(x in data.columns for x in ['MACD', 'Signal']):
            if data['MACD'].iloc[-1] > data['Signal'].iloc[-1] and \
               data['MACD'].iloc[-2] <= data['Signal'].iloc[-2]:
                signals.append({"indicator": "MACD", "signal": "BUY", "value": data['MACD'].iloc[-1]})
            elif data['MACD'].iloc[-1] < data['Signal'].iloc[-1] and \
                 data['MACD'].iloc[-2] >= data['Signal'].iloc[-2]:
                signals.append({"indicator": "MACD", "signal": "SELL", "value": data['MACD'].iloc[-1]})

        return signals
