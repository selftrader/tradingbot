import joblib
import numpy as np
from strategies.strategy import StrategyEngine

class Predictor:
    def __init__(self, model_path="models/trade_model.pkl"):
        try:
            self.model = joblib.load(model_path)
        except FileNotFoundError:
            raise Exception(f"Model file not found at {model_path}")

    def predict_live_trade(self, market_data, options_data=None):
        """AI Model Predicts Trade Signal: BUY / SELL / HOLD"""
        strategy_engine = StrategyEngine(market_data, options_data)
        
        # First, try the breakout strategy
        strategy_signal = strategy_engine.breakout_trading()
        if strategy_signal != "HOLD":
            return strategy_signal

        # Otherwise, apply the AI model based on live features
        live_features = [
            market_data["Close"],
            market_data["RSI"],
            market_data["MACD"],
            market_data["SMA_50"],
            market_data["Volume"]
        ]
        return self.model.predict([live_features])[0]  # Returns "BUY" / "SELL" / "HOLD"
