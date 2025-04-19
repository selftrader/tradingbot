import joblib
import pandas as pd

model = joblib.load("models/fib_ai_model.pkl")


def detect_fib_trade_with_ai(df):
    high = df["High"].max()
    low = df["Low"].min()
    diff = high - low

    levels = {
        "0.0": high,
        "0.236": high - 0.236 * diff,
        "0.382": high - 0.382 * diff,
        "0.5": high - 0.5 * diff,
        "0.618": high - 0.618 * diff,
        "1.0": low,
    }

    df["ema_20"] = df["Close"].ewm(span=20).mean()
    df["rsi_14"] = (
        df["Close"].rolling(14).apply(lambda x: (x[-1] - x.mean()) / x.std() * 100)
    )
    df["volatility"] = df["Close"].rolling(10).std()
    df.dropna(inplace=True)

    signals = []

    for _, row in df.iterrows():
        close = row["Close"]
        if close > levels["0.382"]:  # In breakout zone
            features = [[row["Close"], row["ema_20"], row["rsi_14"], row["volatility"]]]
            prediction = model.predict(features)
            if prediction[0] == 1:
                signals.append(
                    {
                        "timestamp": row["timestamp"],
                        "price": close,
                        "type": "BUY",
                        "signal": "FIB_AI_APPROVED",
                    }
                )

    return signals, levels
