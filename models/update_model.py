import pandas as pd
import joblib
import os
from sklearn.ensemble import RandomForestClassifier

MODEL_PATH = "models/trading_model.pkl"
TRADE_HISTORY_PATH = "data/trade_history.csv"

def retrain_model():
    """Retrains AI using executed trade data to improve accuracy over time."""

    if not os.path.exists(TRADE_HISTORY_PATH):
        print("❌ No trade history found for retraining.")
        return

    df = pd.read_csv(TRADE_HISTORY_PATH)

    # Ensure required columns exist
    required_cols = ["SMA_50", "EMA_50", "RSI", "MACD", "Close", "Target"]
    missing_cols = [col for col in required_cols if col not in df.columns]

    if missing_cols:
        print(f"❌ Missing columns in trade history: {missing_cols}")
        return

    X = df[["SMA_50", "EMA_50", "RSI", "MACD"]]
    y = df["Target"]

    # Retrain Model
    model = RandomForestClassifier(n_estimators=100)
    model.fit(X, y)

    joblib.dump(model, MODEL_PATH)
    print(f"✅ AI Model Retrained & Saved: {MODEL_PATH}")

if __name__ == "__main__":
    retrain_model()
