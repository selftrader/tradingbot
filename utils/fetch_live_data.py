import requests
import pandas as pd
import time

API_URL = "https://query1.finance.yahoo.com/v8/finance/chart/{}?interval=1d"

def fetch_live_stock_data(symbol, retries=3):
    """Fetches live market data with retry mechanism."""
    for attempt in range(retries):
        try:
            url = API_URL.format(symbol)
            response = requests.get(url)

            # ✅ Check for valid response
            if response.status_code != 200:
                print(f"⚠️ Attempt {attempt+1}: HTTP {response.status_code} for {symbol}")
                time.sleep(2 ** attempt)  # Exponential Backoff
                continue

            data = response.json()

            # ✅ Validate JSON response
            if "chart" not in data or "result" not in data["chart"] or not data["chart"]["result"]:
                print(f"⚠️ No valid data found in response for {symbol}. Retrying...")
                time.sleep(2 ** attempt)
                continue

            result = data["chart"]["result"][0]
            indicators = result["indicators"]["quote"][0]
            timestamp = result["timestamp"][-1]

            stock_data = {
                "symbol": symbol,
                "timestamp": timestamp,
                "Close": indicators["close"][-1] if "close" in indicators else None,
                "Open": indicators["open"][-1] if "open" in indicators else None,
                "High": indicators["high"][-1] if "high" in indicators else None,
                "Low": indicators["low"][-1] if "low" in indicators else None,
                "Volume": indicators["volume"][-1] if "volume" in indicators else None
            }

            # ✅ Ensure all required values are available
            if None in stock_data.values():
                print(f"⚠️ Incomplete data for {symbol}. Skipping...")
                return None

            return pd.DataFrame([stock_data])

        except requests.exceptions.RequestException as e:
            print(f"❌ API Request Error for {symbol}: {e}")
        except Exception as e:
            print(f"❌ Unexpected Error Fetching Data for {symbol}: {e}")

        time.sleep(2 ** attempt)  # Exponential backoff

    print(f"❌ Failed to fetch data for {symbol} after {retries} attempts.")
    return None
