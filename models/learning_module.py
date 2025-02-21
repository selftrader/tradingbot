import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from db.database import SessionLocal
from db.models import Trade

class LearningModule:
    def retrain_model(self, instrument):
        """Retrains AI model using past trade data for the selected instrument"""
        db = SessionLocal()
        trade_history = db.query(Trade).filter(Trade.instrument == instrument).all()
        db.close()

        X, y = [], []
        for trade in trade_history:
            features = [trade.entry_price, trade.exit_price, trade.profit_loss]
            label = 1 if trade.profit_loss > 0 else 0
            X.append(features)
            y.append(label)

        X, y = np.array(X), np.array(y)
        if len(X) > 50:
            model = RandomForestClassifier(n_estimators=100)
            model.fit(X, y)
            joblib.dump(model, f"models/{instrument}_model.pkl")
