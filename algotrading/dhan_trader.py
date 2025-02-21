# File: dhan_trader.py
from dhanhq import dhanhq
import pandas as pd
from datetime import datetime, timedelta

class DhanTrader:
    def __init__(self, client_id, access_token):
        """Initialize DhanHQ connection"""
        self.dhan = dhanhq(client_id=client_id, access_token=access_token)

    def fetch_live_price(self, symbol):
        """Fetch live price data from DhanHQ"""
        try:
            quote = self.dhan.get_quote(symbol)
            return {
                'ltp': quote['last_traded_price'],
                'change': quote['change'],
                'change_percentage': quote['change_percentage'],
                'volume': quote['volume']
            }
        except Exception as e:
            print(f"Error fetching live price for {symbol}: {e}")
            return None

    def fetch_market_data(self, symbol):
        """Fetch market data (historical)"""
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=30)
            historical_data = self.dhan.historical_data(
                symbol=symbol,
                from_date=start_date.strftime('%Y-%m-%d'),
                to_date=end_date.strftime('%Y-%m-%d'),
                interval='1d'
            )
            df = pd.DataFrame(historical_data)
            print(f"\nFetched market data for {symbol}:")
            print(df.tail())
            return df
        except Exception as e:
            print(f"Error fetching market data for {symbol}: {e}")
            return None
