import requests
import pandas as pd

API_HOST = "apidojo-yahoo-finance-v1.p.rapidapi.com"
API_KEY = "19e84ccb13msh37426e60103a9e5p1e5f3fjsn8fa006a65ef2"  # Replace with your RapidAPI Key

class YahooFinanceHistoricalData:
    def __init__(self):
        self.base_url = f"https://{API_HOST}/stock/v3/get-historical-data"

    def fetch_historical_data(self, symbol):
        """Fetches historical stock data for AI training"""
        querystring = {
            "region": "IN",
            "symbol": symbol
        }
        headers = {
            "X-RapidAPI-Key": API_KEY,
            "X-RapidAPI-Host": API_HOST
        }

        response = requests.get(self.base_url, headers=headers, params=querystring)

        if response.status_code == 200:
            data = response.json()
            if "prices" in data:
                df = pd.DataFrame(data["prices"])
                df = df[["date", "open", "high", "low", "close", "volume"]]
                df["date"] = pd.to_datetime(df["date"], unit="s")  # Convert timestamp to date
                df.to_csv(f"data/{symbol}_historical.csv", index=False)
                print(f"✅ Historical data saved: data/{symbol}_historical.csv")
                return df
            else:
                print("⚠️ No valid data found:", data)
                return None
        else:
            print(f"❌ Error fetching data for {symbol}: HTTP {response.status_code}")
            return None

# Example Usage
if __name__ == "__main__":
    fetcher = YahooFinanceHistoricalData()
    fetcher.fetch_historical_data("TATAMOTORS.NS")  # Fetch historical data for Tata Motors (NSE)
