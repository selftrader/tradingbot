from typing import Dict, List
import yfinance as yf
import pandas as pd
import logging
from datetime import datetime, timedelta
from .broker_service import BrokerInterface

logger = logging.getLogger(__name__)

class LiveMarketService:
    def __init__(self, broker_service: BrokerInterface):
        self.broker = broker_service
        self.data_cache = {}
        self.update_interval = 60  # 1 minute
        self.last_update = {}
    
    async def get_live_data(self, symbol: str) -> Dict:
        """Get real-time market data from broker"""
        try:
            quote = await self.broker.get_live_quote(symbol)
            
            # Calculate technical indicators
            self.data_cache[symbol] = {
                'price': quote['price'],
                'volume': quote['volume'],
                'timestamp': quote['timestamp'],
                'indicators': await self._calculate_indicators(symbol, quote)
            }
            
            return self.data_cache[symbol]
            
        except Exception as e:
            logger.error(f"Error fetching live data for {symbol}: {e}")
            raise