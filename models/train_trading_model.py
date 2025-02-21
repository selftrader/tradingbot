import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import joblib
import yfinance as yf
import logging

logger = logging.getLogger(__name__)

class TradingModelTrainer:
    def __init__(self):
        self.model_path = "models/saved/trading_model.joblib"
        self.model = RandomForestClassifier(
            n_estimators=100,
            random_state=42
        )

    def prepare_features(self, data: pd.DataFrame) -> pd.DataFrame:
        """Prepare features for model training"""
        df = data.copy()
        
        # Technical indicators
        df['SMA20'] = df['Close'].rolling(window=20).mean()
        df['SMA50'] = df['Close'].rolling(window=50).mean()
        df['RSI'] = self._calculate_rsi(df['Close'])
        
        # Price changes
        df['Returns'] = df['Close'].pct_change()
        df['Volatility'] = df['Returns'].rolling(window=20).std()
        
        # Volume indicators
        df['Volume_MA'] = df['Volume'].rolling(window=20).mean()
        df['Volume_Ratio'] = df['Volume'] / df['Volume_MA']
        
        # Target variable (1 for price increase, 0 for decrease)
        df['Target'] = (df['Close'].shift(-1) > df['Close']).astype(int)
        
        return df.dropna()

    def _calculate_rsi(self, prices: pd.Series, period: int = 14) -> pd.Series:
        """Calculate RSI indicator"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))

    def train_model(self, symbols: list = None):
        """Train the trading model"""
        if symbols is None:
            symbols = ["RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS"]
        
        all_data = []
        for symbol in symbols:
            try:
                data = yf.download(symbol, period="2y", interval="1d")
                if not data.empty:
                    prepared_data = self.prepare_features(data)
                    all_data.append(prepared_data)
                    logger.info(f"Processed data for {symbol}")
            except Exception as e:
                logger.error(f"Error processing {symbol}: {str(e)}")
        
        if not all_data:
            raise ValueError("No training data available")
        
        # Combine all data
        full_data = pd.concat(all_data)
        
        # Prepare features and target
        features = ['SMA20', 'SMA50', 'RSI', 'Returns', 
                   'Volatility', 'Volume_Ratio']
        X = full_data[features]
        y = full_data['Target']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Train model
        self.model.fit(X_train, y_train)
        
        # Save model
        joblib.dump(self.model, self.model_path)
        
        # Print performance metrics
        train_score = self.model.score(X_train, y_train)
        test_score = self.model.score(X_test, y_test)
        logger.info(f"Train accuracy: {train_score:.2f}")
        logger.info(f"Test accuracy: {test_score:.2f}")
        
        return {
            "train_accuracy": train_score,
            "test_accuracy": test_score,
            "model_path": self.model_path
        }