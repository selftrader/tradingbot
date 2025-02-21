import pandas as pd
import numpy as np
import logging
import yfinance as yf

logger = logging.getLogger(__name__)

class TechnicalAnalysis:
    def __init__(self):
        try:
            import pandas_ta as ta
            self.ta = ta
            self.using_pandas_ta = True
            logger.info("Using pandas_ta for technical indicators")
        except ImportError:
            self.using_pandas_ta = False
            logger.warning("pandas_ta not available, using alternative calculations")

    def calculate_indicators(self, data: pd.DataFrame) -> pd.DataFrame:
        """Calculate technical indicators using pandas_ta if available"""
        if self.using_pandas_ta:
            try:
                # Add pandas_ta indicators
                data.ta.rsi(append=True)
                data.ta.macd(append=True)
                data.ta.bbands(append=True)
                return data
            except Exception as e:
                logger.error(f"Error using pandas_ta: {str(e)}")
                return self._calculate_basic_indicators(data)
        else:
            return self._calculate_basic_indicators(data)

    def _calculate_basic_indicators(self, data: pd.DataFrame) -> pd.DataFrame:
        """Calculate basic technical indicators without pandas_ta"""
        try:
            # Calculate RSI
            delta = data['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            data['RSI_14'] = 100 - (100 / (1 + rs))

            # Calculate MACD
            exp1 = data['Close'].ewm(span=12, adjust=False).mean()
            exp2 = data['Close'].ewm(span=26, adjust=False).mean()
            data['MACD'] = exp1 - exp2
            data['Signal'] = data['MACD'].ewm(span=9, adjust=False).mean()

            # Calculate Bollinger Bands
            data['SMA_20'] = data['Close'].rolling(window=20).mean()
            std_dev = data['Close'].rolling(window=20).std()
            data['BB_upper'] = data['SMA_20'] + (std_dev * 2)
            data['BB_lower'] = data['SMA_20'] - (std_dev * 2)

            return data
        except Exception as e:
            logger.error(f"Error calculating basic indicators: {str(e)}")
            return data