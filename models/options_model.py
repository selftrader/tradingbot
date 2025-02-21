import joblib
import numpy as np
from sklearn.ensemble import GradientBoostingClassifier

class OptionsPredictor:
    def __init__(self):
        self.model = joblib.load("models/options_model.pkl")

    def predict_options_movement(self, options_data):
        """Predicts Call/Put movement using Options Data"""
        return self.model.predict([options_data])[0]

    def retrain_options_model(self, trade_history):
        """Retrains model using past options trade data"""
        X, y = [], []
        for trade in trade_history:
            features = [trade["Delta"], trade["Gamma"], trade["IV"], trade["OI"]]
            label = 1 if trade["profit_loss"] > 0 else 0
            X.append(features)
            y.append(label)

        X, y = np.array(X), np.array(y)
        if len(X) > 50:
            self.model.fit(X, y)
            joblib.dump(self.model, "models/options_model.pkl")
