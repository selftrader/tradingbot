import requests
import pandas as pd
import os

class DataLoader:
    def __init__(self, source="yahoo"):
        """Initialize data source: yahoo, nse, zerodha, dhan"""
        self.source = source.lower()

    def fetch_historical_data(self, symbol, start_date, end_date, interval="1d", instrument_type="index"):
        """Fetches historical stock, index, or options data"""

        # Select API based on data source
        if self.source == "yahoo":
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?period1={start_date}&period2={end_date}&interval={interval}"
        elif self.source == "zerodha":
            url = f"https://api.kite.trade/instruments/{symbol}/historical/{start_date}/{end_date}/{interval}"
        elif self.source == "dhan":
            url = f"https://api.dhan.co/marketdata/{symbol}/historical/{start_date}/{end_date}/{interval}"
        elif self.source == "nse":
            url = f"https://nseindia.com/api/historical/{symbol}?start={start_date}&end={end_date}&interval={interval}"
        else:
            raise ValueError("Invalid Data Source")

        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()

            # Process data differently for each instrument type
            if instrument_type == "index":
                df = pd.DataFrame(data["chart"]["result"][0]["indicators"]["quote"][0])
            elif instrument_type == "options":
                df = pd.DataFrame(data["options_chain"]["result"])
            elif instrument_type == "stocks":
                df = pd.DataFrame(data["chart"]["result"][0]["indicators"]["quote"][0])
            elif instrument_type == "sectoral":
                df = pd.DataFrame(data["sector_trends"]["result"])
            else:
                raise ValueError("Invalid instrument type")

            return df
        else:
            raise Exception(f"Error fetching data for {symbol}")

    def save_data_to_csv(self, data, filename):
        """Saves historical data to CSV"""
        os.makedirs("data", exist_ok=True)
        filepath = f"data/{filename}.csv"
        data.to_csv(filepath, index=False)
        print(f"Data saved to {filepath}")
