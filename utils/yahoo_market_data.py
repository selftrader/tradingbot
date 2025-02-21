import yfinance as yf
import pandas as pd
import os

class YahooMarketData:
    def __init__(self):
        self.report = []

        # Ensure 'data/' directory exists
        os.makedirs("data", exist_ok=True)

    def fetch_live_price(self, symbol):
        """Fetches the live price of a stock/index"""
        try:
            stock = yf.Ticker(symbol)
            live_price = stock.history(period="1d")["Close"].iloc[-1]
            print(f"📈 {symbol} Live Price: {live_price}")
            self.report.append(f"{symbol} Live Price: {live_price}")
            return live_price
        except Exception as e:
            print(f"❌ Error fetching live price for {symbol}: {e}")
            self.report.append(f"❌ Error fetching live price for {symbol}: {e}")
            return None

    def fetch_historical_data(self, symbol, start="2019-01-01", end="2024-01-01", interval="1d"):
        """Fetches historical market data for a stock/index"""
        try:
            df = yf.download(symbol, start=start, end=end, interval=interval)
            if df.empty:
                print(f"⚠️ No data found for {symbol}")
                self.report.append(f"⚠️ No data found for {symbol}")
                return None
            
            # Save to CSV
            filename = f"data/{symbol}_historical.csv"
            df.to_csv(filename)
            print(f"✅ Historical data saved: {filename}")
            self.report.append(f"✅ Historical data saved: {filename}")
            return df
        except Exception as e:
            print(f"❌ Error fetching historical data for {symbol}: {e}")
            self.report.append(f"❌ Error fetching historical data for {symbol}: {e}")
            return None

    def fetch_options_data(self, symbol):
        """Fetches options chain for a stock/index"""
        try:
            stock = yf.Ticker(symbol)
            expirations = stock.options  # Get available expiration dates
            if not expirations:
                print(f"⚠️ No options data found for {symbol}")
                self.report.append(f"⚠️ No options data found for {symbol}")
                return None
            
            nearest_expiry = expirations[0]
            options_chain = stock.option_chain(nearest_expiry)

            # Save calls and puts
            calls_filename = f"data/{symbol}_calls_{nearest_expiry}.csv"
            puts_filename = f"data/{symbol}_puts_{nearest_expiry}.csv"
            options_chain.calls.to_csv(calls_filename, index=False)
            options_chain.puts.to_csv(puts_filename, index=False)

            print(f"✅ Options data saved: {calls_filename}, {puts_filename}")
            self.report.append(f"✅ Options data saved: {calls_filename}, {puts_filename}")
            return options_chain
        except Exception as e:
            print(f"❌ Error fetching options data for {symbol}: {e}")
            self.report.append(f"❌ Error fetching options data for {symbol}: {e}")
            return None

    def save_report(self):
        """Saves market data report to a file"""
        report_path = "data/market_report.txt"
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("\n".join(self.report))
        print(f"📊 Market Report Saved: {report_path}")

# Example Usage
if __name__ == "__main__":
    market_data = YahooMarketData()

    # Fetch live market prices
    market_data.fetch_live_price("^NSEI")  # NIFTY 50
    market_data.fetch_live_price("^BSESN")  # SENSEX
    market_data.fetch_live_price("RELIANCE.NS")

    # Fetch historical data
    market_data.fetch_historical_data("NIFTY50.NS")
    market_data.fetch_historical_data("RELIANCE.NS")

    # Fetch options chain data
    market_data.fetch_options_data("^NSEI")  # NIFTY 50 Options
    market_data.fetch_options_data("^BANKNIFTY")  # BANKNIFTY Options

    # Save market report
    market_data.save_report()
