import os
import logging
from typing import Optional
from upstox_api.api import Upstox
import pandas as pd
import pandas as ta

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

class UpstoxDataFetcher:
    """
    Handles Upstox API authentication, historical data fetching, and indicator computations.
    """
    def __init__(self, api_key: str, api_secret: str, redirect_uri: str) -> None:
        self.api_key = api_key
        self.api_secret = api_secret
        self.redirect_uri = redirect_uri
        self.upstox: Optional[Upstox] = None

    def authenticate(self) -> Upstox:
        """
        Authenticate with Upstox.
        (This simplified version returns a client with the assumed session.)
        """
        # Remove the redirect_uri argument since Upstox.__init__ expects only api_key and api_secret
        session = Upstox(self.api_key, self.api_secret)
        self.upstox = session
        return self.upstox

    def fetch_historical_data(self, symbol: str, start_date: str, end_date: str, interval):
        if self.upstox is None:
            raise Exception("Not authenticated. Please call authenticate() first.")
            
        instrument = self.upstox.get_instrument_by_symbol('NSE_EQ', symbol)
        data = self.upstox.get_ohlc(instrument, interval, start_date, end_date)
        df = pd.DataFrame(data)
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df.set_index('timestamp', inplace=True)
        logger.info(f"Fetched data for {symbol}")
        return df

    def compute_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        if 'close' not in df.columns:
            raise ValueError("DataFrame must contain a 'close' column.")
        df['RSI'] = ta.rsi(df['close'])
        df['EMA_20'] = ta.ema(df['close'], length=20)
        high = df['close'].max()
        low = df['close'].min()
        diff = high - low
        df['Fib_23.6'] = high - 0.236 * diff
        df['Fib_38.2'] = high - 0.382 * diff
        df['Fib_61.8'] = high - 0.618 * diff
        return df

    def save_data(self, df: pd.DataFrame, symbol: str):
        folder_path = os.path.join(os.getcwd(), 'data', 'processed', symbol)
        os.makedirs(folder_path, exist_ok=True)
        file_path = os.path.join(folder_path, f"{symbol}_historical_data.csv")
        df.to_csv(file_path)
        logger.info(f"Data saved to {file_path}")

def main() -> None:
    # Replace these with your actual Upstox credentials or load from a secure configuration.
    API_KEY = 'your_api_key'
    API_SECRET = 'your_api_secret'
    REDIRECT_URI = 'your_redirect_uri'

    # Parameters for data fetching
    symbol = 'RELIANCE'
    start_date = '2020-01-01'
    end_date = '2020-01-10'

    fetcher = UpstoxDataFetcher(API_KEY, API_SECRET, REDIRECT_URI)

    try:
        fetcher.authenticate()
        df = fetcher.fetch_historical_data(symbol, start_date, end_date, '15minute')
        df = fetcher.compute_indicators(df)
        fetcher.save_data(df, symbol)
    except Exception as e:
        logger.error("An error occurred during the data fetching process.", exc_info=True)


if __name__ == "__main__":
    main()
