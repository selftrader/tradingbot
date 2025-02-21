import yfinance as yf
import pandas as pd
import os

class SectoralDataFetcher:
    def __init__(self):
        self.report = []
        os.makedirs("data/sectoral", exist_ok=True)  # Ensure 'data/sectoral/' directory exists

    def fetch_historical_data(self, symbol, name, start="2019-01-01", end="2024-01-01", interval="1d"):
        """Fetches historical sectoral market data for AI model training."""
        try:
            print(f"📡 Fetching historical data for {name} ({symbol})...")
            df = yf.download(symbol, start=start, end=end, interval=interval)
            if df.empty:
                print(f"⚠️ No data found for {name}")
                self.report.append(f"⚠️ No data found for {name}")
                return None
            
            filename = f"data/sectoral/{name}_historical.csv"
            df.to_csv(filename)
            print(f"✅ Sectoral Data Saved: {filename}")
            self.report.append(f"✅ Sectoral Data Saved: {filename}")
            return df
        except Exception as e:
            print(f"❌ Error fetching data for {name}: {e}")
            self.report.append(f"❌ Error fetching data for {name}: {e}")
            return None

    def fetch_live_price(self, symbol, name):
        """Fetch live sectoral index prices."""
        try:
            stock = yf.Ticker(symbol)
            live_price = stock.history(period="1d")["Close"].iloc[-1]
            print(f"📈 {name} Live Price: {live_price}")
            self.report.append(f"{name} Live Price: {live_price}")
            return live_price
        except Exception as e:
            print(f"❌ Error fetching live price for {name}: {e}")
            self.report.append(f"❌ Error fetching live price for {name}: {e}")
            return None

    def save_report(self):
        """Save fetch report."""
        report_path = "data/sectoral/sectoral_fetch_report.txt"
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("\n".join(self.report))
        print(f"📊 Sectoral Fetch Report Saved: {report_path}")

# Example Usage
if __name__ == "__main__":
    fetcher = SectoralDataFetcher()

    # ✅ Fetch Historical Data for All Sectoral Indices
    sectors = {
        "NIFTY_IT": "^CNXIT",
        "NIFTY_PHARMA": "^CNXPHARMA",
        "NIFTY_BANK": "^BANKNIFTY",
        "NIFTY_AUTO": "^CNXAUTO",
        "NIFTY_FMCG": "^CNXFMCG"
    }

    for name, symbol in sectors.items():
        fetcher.fetch_historical_data(symbol, name)

    # ✅ Fetch Live Prices for All Sectors
    for name, symbol in sectors.items():
        fetcher.fetch_live_price(symbol, name)

    # ✅ Save Fetch Report
    fetcher.save_report()
