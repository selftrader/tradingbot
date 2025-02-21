import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier

class IndexPredictor:
    def __init__(self):
        self.model = joblib.load("models/index_model.pkl")

    def predict_index_movement(self, market_data):
        """Predicts market movement for Index"""
        return self.model.predict([market_data])[0]

    def retrain_index_model(self, trade_history):
        """Retrains model using past index trade data"""
        X, y = [], []
        for trade in trade_history:
            features = [trade["RSI"], trade["MACD"], trade["VWAP"], trade["Volume"]]
            label = 1 if trade["profit_loss"] > 0 else 0
            X.append(features)
            y.append(label)

        X, y = np.array(X), np.array(y)
        if len(X) > 50:
            self.model.fit(X, y)
            joblib.dump(self.model, "models/index_model.pkl")
