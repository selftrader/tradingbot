import requests
import pandas as pd
from datetime import datetime

def fetch_ohlcv_data(symbol, exchange, from_date, to_date):
    # 🔁 Call Upstox historical endpoint (replace with actual token handling)
    url = "https://api.upstox.com/v2/historical-candle"
    headers = {"Authorization": f"Bearer YOUR_UPSTOX_ACCESS_TOKEN"}
    params = {
        "instrument_key": f"{exchange}_EQ|{symbol}",
        "interval": "1day",
        "from": from_date,
        "to": to_date
    }
    response = requests.get(url, headers=headers, params=params)
    candles = response.json().get("data", {}).get("candles", [])

    df = pd.DataFrame(candles, columns=["timestamp", "open", "high", "low", "close", "volume"])
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df
