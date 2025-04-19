import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator
import os


def train_fib_ai_model(csv_path, model_path="models/fib_ai_model.pkl"):
    df = pd.read_csv(csv_path)
    df.dropna(inplace=True)

    # Step 1: Calculate indicators (features)
    df["ema_20"] = EMAIndicator(close=df["Close"], window=20).ema_indicator()
    df["rsi_14"] = RSIIndicator(close=df["Close"], window=14).rsi()
    df["volatility"] = df["Close"].rolling(window=10).std()

    # Step 2: Create target (did price go up in next 5 candles?)
    df["target"] = (df["Close"].shift(-5) > df["Close"]).astype(int)
    df.dropna(inplace=True)

    features = ["Close", "ema_20", "rsi_14", "volatility"]
    X = df[features]
    y = df["target"]

    # Step 3: Train model
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    os.makedirs(os.path.dirname(model_path), exist_ok=True)
    joblib.dump(model, model_path)
    print(f"✅ Model trained and saved to {model_path}")
