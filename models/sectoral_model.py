import os
import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier

class SectoralPredictor:
    def __init__(self):
        model_path = "models/sectoral_model.pkl"
        if os.path.exists(model_path):
            self.model = joblib.load(model_path)
            print(f"Loaded model from {model_path}")
        else:
            # If no model exists, initialize a new one and save it as a placeholder.
            self.model = RandomForestClassifier()
            joblib.dump(self.model, model_path)
            print(f"Model file not found. A new model has been created and saved at {model_path}")

    def predict_sectoral_trend(self, sectoral_data):
        """
        Predicts Market Movement for sectors using input data.
        Expects sectoral_data to be a list of features, e.g.:
            [Sector_RSI, Institutional_Buying, FII_DII_Activity]
        """
        try:
            prediction = self.model.predict([sectoral_data])[0]
            return prediction
        except Exception as e:
            print("Error predicting sectoral trend:", e)
            return None

    def retrain_sectoral_model(self, trade_history):
        """
        Retrains the model using past sectoral trade data.
        Each item in trade_history should be a dictionary with keys:
            "Sector_RSI", "Institutional_Buying", "FII_DII_Activity", and "profit_loss"
        The label is set to 1 if 'profit_loss' > 0, otherwise 0.
        """
        X, y = [], []
        for trade in trade_history:
            features = [
                trade["Sector_RSI"],
                trade["Institutional_Buying"],
                trade["FII_DII_Activity"]
            ]
            label = 1 if trade["profit_loss"] > 0 else 0
            X.append(features)
            y.append(label)

        X, y = np.array(X), np.array(y)
        if len(X) > 50:
            self.model.fit(X, y)
            joblib.dump(self.model, "models/sectoral_model.pkl")
            print("Sectoral model has been retrained and saved.")
        else:
            print("Not enough data to retrain the model. Need at least 50 samples.")
