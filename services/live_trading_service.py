import asyncio
import pandas as pd
import numpy as np
import yfinance as yf
import joblib
from datetime import datetime, timedelta
import logging
from typing import Dict, List
from database.connection import get_db
from models.database_models import Trade, Position  # Changed import statement

logger = logging.getLogger(__name__)

class LiveTradingService:
    def __init__(self):
        self.model = self._load_model()
        self.confidence_threshold = 0.7
        self.position_size = 100000  # ₹1 Lakh per trade
        self.max_positions = 5
        self.stop_loss_pct = 0.02  # 2% stop loss
        
    def _load_model(self):
        try:
            return joblib.load("models/saved/trading_model.joblib")
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            return None
            
    async def execute_live_trading(self, symbols: List[str]):
        """Main live trading loop"""
        while True:
            try:
                for symbol in symbols:
                    # 1. Get real-time data
                    data = self._get_live_data(symbol)
                    
                    # 2. Generate features
                    features = self._prepare_live_features(data)
                    
                    # 3. Get model prediction
                    signal = self._get_trading_signal(features)
                    
                    # 4. Execute trade if conditions met
                    if signal['confidence'] > self.confidence_threshold:
                        await self._execute_trade(symbol, signal)
                        
                    # 5. Monitor open positions
                    await self._monitor_positions()
                    
                # Wait for next iteration
                await asyncio.sleep(300)  # 5-minute intervals
                    
            except Exception as e:
                logger.error(f"Live trading error: {e}")
                await asyncio.sleep(60)
                
    def _get_live_data(self, symbol: str) -> pd.DataFrame:
        """Fetch real-time market data"""
        try:
            # Get intraday data (5-minute intervals)
            data = yf.download(
                symbol,
                period="5d",
                interval="5m"
            )
            return data
        except Exception as e:
            logger.error(f"Error fetching live data: {e}")
            raise
            
    def _prepare_live_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """Prepare features for live prediction"""
        df = data.copy()
        
        # Calculate technical indicators
        df['SMA20'] = df['Close'].rolling(window=20).mean()
        df['SMA50'] = df['Close'].rolling(window=50).mean()
        df['RSI'] = self._calculate_rsi(df['Close'])
        df['Returns'] = df['Close'].pct_change()
        df['Volatility'] = df['Returns'].rolling(window=20).std()
        df['Volume_Ratio'] = df['Volume'] / df['Volume'].rolling(window=20).mean()
        
        return df.dropna()
        
    def _get_trading_signal(self, features: pd.DataFrame) -> Dict:
        """Generate trading signal from model"""
        if not self.model:
            return {"action": "HOLD", "confidence": 0}
            
        X = features[self.features].iloc[-1:].values
        prob = self.model.predict_proba(X)[0]
        
        return {
            "action": "BUY" if prob[1] > self.confidence_threshold else "SELL",
            "confidence": float(max(prob)),
            "timestamp": datetime.now().isoformat()
        }
        
    async def _execute_trade(self, symbol: str, signal: Dict):
        """Execute trade in live market"""
        db = next(get_db())
        try:
            # Check existing positions
            positions = db.query(Position).filter(
                Position.symbol == symbol,
                Position.is_active == True
            ).count()
            
            if positions >= self.max_positions:
                logger.info(f"Max positions reached for {symbol}")
                return
                
            # Calculate position size
            current_price = yf.Ticker(symbol).info['regularMarketPrice']
            quantity = int(self.position_size / current_price)
            
            # Place order
            trade = Trade(
                symbol=symbol,
                quantity=quantity,
                price=current_price,
                trade_type=signal['action'],
                stop_loss=current_price * (1 - self.stop_loss_pct),
                confidence=signal['confidence']
            )
            
            db.add(trade)
            db.commit()
            
            logger.info(f"Executed {signal['action']} for {symbol} "
                       f"qty: {quantity} @ {current_price}")
                       
        except Exception as e:
            logger.error(f"Trade execution error: {e}")
            db.rollback()
        finally:
            db.close()