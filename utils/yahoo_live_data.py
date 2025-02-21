import requests
import json

# Set up RapidAPI credentials
API_HOST = "apidojo-yahoo-finance-v1.p.rapidapi.com"
API_KEY = "19e84ccb13msh37426e60103a9e5p1e5f3fjsn8fa006a65ef2"  # Replace with your RapidAPI Key

class YahooFinanceLiveData:
    def __init__(self):
        self.base_url = f"https://{API_HOST}/market/v2/get-quotes"

    def fetch_live_data(self, symbols):
        """Fetches live stock data for NSE/BSE"""
        querystring = {
            "region": "IN",
            "symbols": ",".join(symbols)
        }
        headers = {
            "X-RapidAPI-Key": API_KEY,
            "X-RapidAPI-Host": API_HOST
        }

        response = requests.get(self.base_url, headers=headers, params=querystring)

        if response.status_code == 200:
            data = response.json()
            print("✅ Live Data Fetched:", json.dumps(data, indent=2))
            return data
        else:
            print(f"❌ Error fetching data: HTTP {response.status_code}")
            return None

# Example Usage
if __name__ == "__main__":
    fetcher = YahooFinanceLiveData()
    live_data = fetcher.fetch_live_data(["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS"])  # Fetch NSE stock data
