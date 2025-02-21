import requests
import pandas as pd
import os
import time

# API Credentials (Replace with your actual API Key from RapidAPI)
API_HOST = "apidojo-yahoo-finance-v1.p.rapidapi.com"
API_KEY = os.getenv("YAHOO_FINANCE_API_KEY")  # Store API Key securely

class YahooFinanceHistoricalData:
    def __init__(self, instrument_type, years=5):
        self.base_url = f"https://{API_HOST}/stock/v3/get-historical-data"
        self.instrument_type = instrument_type.lower()
        self.years = years
        self.report = []

    def fetch_historical_data(self, symbol):
        """Fetches 3-5 years of historical data for AI training with rate limiting & authentication check"""
        querystring = {"region": "IN", "symbol": symbol}
        headers = {
            "X-RapidAPI-Key": API_KEY,
            "X-RapidAPI-Host": API_HOST
        }

        print(f"📡 Fetching {self.years} years of historical data for {symbol} ({self.instrument_type})...")

        for attempt in range(5):  # Retry up to 5 times in case of 429 error
            response = requests.get(self.base_url, headers=headers, params=querystring)

            if response.status_code == 200:
                data = response.json()
                if "prices" in data:
                    df = pd.DataFrame(data["prices"])

                    # Select only relevant columns based on instrument type
                    if self.instrument_type in ["index", "stocks"]:
                        df = df[["date", "open", "high", "low", "close", "volume"]]
                    elif self.instrument_type == "options":
                        df = df[["date", "open", "high", "low", "close", "volume", "openInterest", "impliedVolatility"]]

                    # Convert timestamp to readable date format
                    df["date"] = pd.to_datetime(df["date"], unit="s")

                    # Keep only last 3-5 years of data
                    df = df[df["date"] >= pd.Timestamp.today() - pd.DateOffset(years=self.years)]

                    # Ensure 'data/' folder exists before saving
                    os.makedirs("data", exist_ok=True)

                    # Save filtered data
                    filename = f"data/{symbol}_{self.instrument_type}_historical.csv"
                    df.to_csv(filename, index=False)

                    # Add to report
                    self.report.append(f"✅ Data fetched & saved: {filename}")
                    self.report.append(f"   Total Rows: {len(df)}")
                    self.report.append(f"   Start Date: {df['date'].min()}")
                    self.report.append(f"   End Date: {df['date'].max()}\n")

                    print(f"✅ Historical data saved: {filename}")
                    return df

                else:
                    self.report.append(f"⚠️ No valid data found for {symbol}")
                    print("⚠️ No valid data found:", data)
                    return None

            elif response.status_code == 401:  # Unauthorized
                print("❌ ERROR: Invalid API Key. Please verify your API credentials.")
                self.report.append(f"❌ ERROR: API Key Invalid for {symbol}. Check your credentials.")
                return None

            elif response.status_code == 429:  # Too Many Requests (Rate Limit Exceeded)
                print(f"⏳ Rate limit exceeded for {symbol}. Retrying in {2 ** attempt} seconds...")
                time.sleep(2 ** attempt)  # Exponential backoff (2s, 4s, 8s, etc.)
                continue

            else:
                print(f"❌ Error fetching data for {symbol}: HTTP {response.status_code}")
                self.report.append(f"❌ Error fetching data for {symbol}: HTTP {response.status_code}")
                return None

        print(f"❌ Failed to fetch data for {symbol} after multiple attempts.")
        self.report.append(f"❌ Failed to fetch data for {symbol} after multiple attempts.")
        return None

    def save_report(self):
        """Saves the fetch report in `data/fetch_report.txt` with UTF-8 encoding"""
        report_path = "data/fetch_report.txt"
        with open(report_path, "w", encoding="utf-8") as f:  # Use UTF-8 encoding to fix Unicode error
            f.write("\n".join(self.report))
        print(f"📊 Fetch Report Saved: {report_path}")


# Example Usage
if __name__ == "__main__":
    fetcher = YahooFinanceHistoricalData(instrument_type="index", years=5)
    fetcher.fetch_historical_data("NIFTY50.NS")  # Fetch NIFTY50 Data
    fetcher.fetch_historical_data("BANKNIFTY.NS")  # Fetch BANKNIFTY Data
    fetcher.fetch_historical_data("^BSESN")  # Fetch Sensex Data

    fetcher = YahooFinanceHistoricalData(instrument_type="options", years=5)
    fetcher.fetch_historical_data("NIFTY22500CE.NFO")  # Fetch NIFTY Call Option
    fetcher.fetch_historical_data("BANKNIFTY22500PE.NFO")  # Fetch BANKNIFTY Put Option

    # Save Fetch Report
    fetcher.save_report()
