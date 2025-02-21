# File: run_trading.py
from config import CLIENT_ID, ACCESS_TOKEN, SYMBOLS_TO_TRADE
from dhan_trader import DhanTrader
from datetime import datetime
import pytz
import time

def is_market_open():
    """Check if market is open based on IST"""
    # Define the time zone (Indian Standard Time)
    ist = pytz.timezone('Asia/Kolkata')

    # Get current time in IST
    current_time = datetime.now(ist).time()
    market_start = datetime.strptime("09:15:00", "%H:%M:%S").time()
    market_end = datetime.strptime("15:30:00", "%H:%M:%S").time()

    # Return True if current time is within market hours
    return market_start <= current_time <= market_end

def main():
    # Initialize the trader object
    trader = DhanTrader(CLIENT_ID, ACCESS_TOKEN)
    print("Trading system initialized...")

    try:
        while True:
            if is_market_open():
                print("\nMarket is OPEN.")
            else:
                print("\nMarket is CLOSED. Fetching live data...")

            for symbol in SYMBOLS_TO_TRADE:
                print(f"\nFetching live data for {symbol}...")

                # Fetch live price data
                price_data = trader.fetch_live_price(symbol)

                if price_data:
                    print(f"\n{symbol} Live Market Data:")
                    print(f"Current Price: {price_data['ltp']}")
                    print(f"Price Change: {price_data['change']} ({price_data['change_percentage']}%)")
                    print(f"Volume: {price_data['volume']}")
                else:
                    print(f"Failed to fetch data for {symbol}")

                # Fetch additional market data if needed
                # data = trader.fetch_market_data(symbol)

                time.sleep(2)  # Delay between symbols for rate-limiting

            # Wait 30 seconds before fetching data again
            time.sleep(30)

    except KeyboardInterrupt:
        print("\nStopping trading system...")

    except Exception as e:
        print(f"Error in main loop: {e}")

if __name__ == "__main__":
    main()
