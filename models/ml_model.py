import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from typing import Dict, List, Tuple

class SectoralMLModel:
    def __init__(self):
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        self.scaler = StandardScaler()
        
    def prepare_features(self, data: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        """Calculate technical features and prepare for model"""
        features = pd.DataFrame()
        
        # Price-based features
        features['returns'] = data['Close'].pct_change()
        features['vol_change'] = data['Volume'].pct_change()
        features['high_low_ratio'] = data['High'] / data['Low']
        
        # Technical indicators
        features['rsi'] = self.calculate_rsi(data['Close'])
        features['macd'], features['macd_signal'] = self.calculate_macd(data['Close'])
        features['bb_position'] = self.calculate_bollinger_position(data['Close'])
        
        # Target variable (1 for up, 0 for down)
        target = (data['Close'].shift(-1) > data['Close']).astype(int)
        
        # Drop NaN values
        features = features.dropna()
        target = target[features.index]
        
        return self.scaler.fit_transform(features), target

    def calculate_rsi(self, prices: pd.Series, period: int = 14) -> pd.Series:
        """Calculate RSI technical indicator"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))

    def calculate_macd(self, prices: pd.Series) -> Tuple[pd.Series, pd.Series]:
        """Calculate MACD indicator"""
        exp1 = prices.ewm(span=12, adjust=False).mean()
        exp2 = prices.ewm(span=26, adjust=False).mean()
        macd = exp1 - exp2
        signal = macd.ewm(span=9, adjust=False).mean()
        return macd, signal

    def calculate_bollinger_position(self, prices: pd.Series, window: int = 20) -> pd.Series:
        """Calculate position within Bollinger Bands"""
        sma = prices.rolling(window=window).mean()
        std = prices.rolling(window=window).std()
        upper = sma + (std * 2)
        lower = sma - (std * 2)
        return (prices - lower) / (upper - lower)

    def analyze_stock(self, data: pd.DataFrame) -> Dict:
        """Analyze a single stock and return predictions with confidence"""
        try:
            # Prepare latest data point for prediction
            latest_features = pd.DataFrame()
            latest_features['returns'] = [data['Close'].pct_change().iloc[-1]]
            latest_features['vol_change'] = [data['Volume'].pct_change().iloc[-1]]
            latest_features['high_low_ratio'] = [data['High'].iloc[-1] / data['Low'].iloc[-1]]
            latest_features['rsi'] = [self.calculate_rsi(data['Close']).iloc[-1]]
            
            macd, signal = self.calculate_macd(data['Close'])
            latest_features['macd'] = [macd.iloc[-1]]
            latest_features['macd_signal'] = [signal.iloc[-1]]
            
            latest_features['bb_position'] = [self.calculate_bollinger_position(data['Close']).iloc[-1]]
            
            # Scale features
            scaled_features = self.scaler.transform(latest_features)
            
            # Make prediction and get probability
            prediction = self.model.predict(scaled_features)[0]
            probability = self.model.predict_proba(scaled_features)[0].max()
            
            return {
                'prediction': int(prediction),
                'probability': float(probability),
                'indicators': {
                    'rsi': float(latest_features['rsi'].iloc[0]),
                    'macd': float(latest_features['macd'].iloc[0]),
                    'macd_signal': float(latest_features['macd_signal'].iloc[0]),
                    'bb_position': float(latest_features['bb_position'].iloc[0])
                }
            }
            
        except Exception as e:
            print(f"Error analyzing stock: {str(e)}")
            return None