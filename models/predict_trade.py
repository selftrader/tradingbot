import pandas as pd
import joblib
import ta
from utils.fetch_live_data import fetch_live_stock_data  # ✅ Import function to get live stock data

MODEL_PATH = "models/trading_model.pkl"

# ✅ Load Model Only Once
if not MODEL_PATH:
    raise Exception("❌ AI Model not found. Please train the model first.")
model = joblib.load(MODEL_PATH)

def preprocess_live_data(stock_data):
    """Preprocesses live stock data before prediction."""

    # ✅ Convert Dictionary Input to Pandas DataFrame
    if isinstance(stock_data, dict):
        stock_data = pd.DataFrame([stock_data])  # Convert dict to DataFrame

    # ✅ Ensure stock_data is a DataFrame
    elif not isinstance(stock_data, pd.DataFrame):
        raise TypeError(f"❌ Expected DataFrame but got {type(stock_data)}")

    # ✅ Ensure 'Close' column exists
    if "Close" not in stock_data.columns:
        raise KeyError("❌ Missing required column: 'Close'")

    # ✅ Convert Close column to float
    stock_data["Close"] = stock_data["Close"].astype(float)

    # ✅ Add Technical Indicators
    stock_data["SMA_50"] = ta.trend.sma_indicator(stock_data["Close"], window=50)
    stock_data["EMA_50"] = ta.trend.ema_indicator(stock_data["Close"], window=50)
    stock_data["RSI"] = ta.momentum.rsi(stock_data["Close"], window=14)
    stock_data["MACD"] = ta.trend.macd(stock_data["Close"])

    # ✅ Fill NaN values
    stock_data.fillna(method="ffill", inplace=True)

    return stock_data

def predict_trade(stock_symbol):
    """Fetches live data, processes it, and predicts BUY/SELL."""

    # ✅ Fetch live stock data (New Fix)
    stock_data = fetch_live_stock_data(stock_symbol)

    if stock_data is None:
        print(f"⚠️ Skipping {stock_symbol} - No Live Data Found")
        return "ERROR"

    df = preprocess_live_data(stock_data)  # ✅ Preprocess Data

    # Select required features
    features = df[["SMA_50", "EMA_50", "RSI", "MACD"]].iloc[-1:].values.reshape(1, -1)

    # ✅ Predict using AI model
    prediction = model.predict(features)[0]
    return "BUY" if prediction == 1 else "SELL"
