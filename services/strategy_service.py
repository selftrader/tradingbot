from sqlalchemy.orm import Session
from typing import List, Dict
import logging
import pandas as pd
import numpy as np
import yfinance as yf
import joblib
from sklearn.ensemble import RandomForestClassifier

logger = logging.getLogger(__name__)

class StrategyService:
    def __init__(self, db: Session):
        self.db = db
        self.model = self._load_model()
        self.confidence_threshold = 0.6

    def _load_model(self) -> RandomForestClassifier:
        """Load the trained model"""
        try:
            return joblib.load("models/saved/trading_model.joblib")
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            return None

    async def analyze_stock(self, symbol: str, timeframe: str = '1d') -> Dict:
        """Analyze stock using both technical and AI predictions"""
        try:
            # Fetch and prepare data
            data = yf.download(symbol, period='1y', interval=timeframe)
            prepared_data = self._prepare_features(data)
            
            # Get AI prediction
            if self.model:
                features = ['SMA20', 'SMA50', 'RSI', 'Returns', 
                          'Volatility', 'Volume_Ratio']
                X = prepared_data[features].iloc[-1:]
                prediction_prob = self.model.predict_proba(X)[0]
                ai_signal = "BUY" if prediction_prob[1] > self.confidence_threshold else \
                           "SELL" if prediction_prob[0] > self.confidence_threshold else "HOLD"
                confidence = max(prediction_prob)
            else:
                ai_signal = self._generate_signals(prepared_data)
                confidence = 0.5
            
            return {
                'symbol': symbol,
                'current_price': data['Close'][-1],
                'signal': ai_signal,
                'confidence': confidence,
                'metrics': {
                    'rsi': prepared_data['RSI'][-1],
                    'sma20': prepared_data['SMA20'][-1],
                    'sma50': prepared_data['SMA50'][-1],
                    'volume': data['Volume'][-1],
                    'returns': prepared_data['Returns'][-1],
                    'volatility': prepared_data['Volatility'][-1]
                }
            }
        except Exception as e:
            logger.error(f"Error analyzing stock {symbol}: {str(e)}")
            raise

    def _calculate_rsi(self, prices: pd.Series, period: int = 14) -> pd.Series:
        """Calculate RSI technical indicator"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))

    def _generate_signals(self, data: pd.DataFrame) -> str:
        """Generate trading signals based on technical analysis"""
        last_row = data.iloc[-1]
        
        # Trading conditions
        rsi_oversold = last_row['RSI'] < 30
        rsi_overbought = last_row['RSI'] > 70
        golden_cross = (last_row['SMA20'] > last_row['SMA50']) and \
                      (data['SMA20'].iloc[-2] <= data['SMA50'].iloc[-2])
        death_cross = (last_row['SMA20'] < last_row['SMA50']) and \
                     (data['SMA20'].iloc[-2] >= data['SMA50'].iloc[-2])
        
        if golden_cross or rsi_oversold:
            return "BUY"
        elif death_cross or rsi_overbought:
            return "SELL"
        return "HOLD"