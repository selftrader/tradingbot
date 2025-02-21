import requests
import json

class LiveDataFetcher:
    def __init__(self, source="dhan"):
        """Initialize the live data source"""
        self.source = source.lower()

    def fetch_live_data(self, symbol):
        """Fetches live stock/index/options market data"""

        if self.source == "nse":
            url = f"https://www.nseindia.com/api/quote-equity?symbol={symbol}"
        elif self.source == "zerodha":
            url = f"https://api.kite.trade/quote?i=NSE:{symbol}"
        elif self.source == "dhan":
            url = f"https://api.dhan.co/marketdata/quotes?symbol={symbol}"
        elif self.source == "yahoo":
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1m"
        else:
            raise ValueError("Invalid Data Source")

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            print("✅ Live Data Fetched:", json.dumps(data, indent=2))
            return data
        else:
            print(f"❌ Error fetching data for {symbol}: HTTP {response.status_code}")
            return None

# Example Usage
if __name__ == "__main__":
    fetcher = LiveDataFetcher(source="dhan")
    live_data = fetcher.fetch_live_data("NIFTY50")
