import yfinance as yf
import pandas as pd
import os
from config import SECTORAL_INDICES  # Import sectoral indices dictionary

class MarketDataFetcher:
    def __init__(self):
        os.makedirs("data/sectoral", exist_ok=True)

    def fetch_historical_data(self, symbol, name, folder, start="2019-01-01", end="2024-01-01", interval="1d"):
        """Fetches historical market data for sectoral indices & constituent stocks"""
        try:
            print(f"📡 Fetching historical data for {name} ({symbol})...")
            df = yf.download(symbol, start=start, end=end, interval=interval)

            if df.empty:
                print(f"⚠️ No valid data found for {name}")
                return None

            os.makedirs(f"data/sectoral/{folder}", exist_ok=True)
            filename = f"data/sectoral/{folder}/{name}_historical.csv"
            df.to_csv(filename)
            print(f"✅ Data Saved: {filename}")
            return df
        except Exception as e:
            print(f"❌ Error fetching data for {name}: {e}")
            return None

    def fetch_constituent_data(self):
        """Fetches historical data for each constituent stock in all sectors."""
        for sector_name, stocks in SECTORAL_INDICES.items():
            sector_dir = f"data/sectoral/{sector_name}"
            os.makedirs(sector_dir, exist_ok=True)

            for stock in stocks:
                try:
                    print(f"📡 Fetching data for {stock} in {sector_name} sector...")
                    df = yf.download(stock, start="2019-01-01", end="2024-01-01", interval="1d")
                    if df.empty:
                        print(f"⚠️ No data found for {stock}")
                        continue

                    filename = f"{sector_dir}/{stock}_historical.csv"
                    df.to_csv(filename)
                    print(f"✅ Data Saved: {filename}")
                except Exception as e:
                    print(f"❌ Error fetching data for {stock}: {e}")

# Example Usage
if __name__ == "__main__":
    fetcher = MarketDataFetcher()

    # ✅ Fetch Historical Data for Constituent Stocks
    fetcher.fetch_constituent_data()
