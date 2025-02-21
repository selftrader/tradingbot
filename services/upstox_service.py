from .broker_service import BrokerInterface
from upstox_api.api import Session
import asyncio
import logging
from typing import Dict, List
from datetime import datetime

logger = logging.getLogger(__name__)

class UpstoxService(BrokerInterface):
    def __init__(self, api_key: str, api_secret: str, redirect_uri: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.redirect_uri = redirect_uri
        self.session = None
        
    async def connect(self):
        """Initialize broker connection"""
        try:
            self.session = Session(self.api_key)
            await self.session.set_redirect_uri(self.redirect_uri)
            await self.session.set_api_secret(self.api_secret)
            code = await self.session.get_authorization_code()
            await self.session.retrieve_access_token(code)
            logger.info("Successfully connected to Upstox")
        except Exception as e:
            logger.error(f"Upstox connection error: {e}")
            raise
    
    async def get_live_quote(self, symbol: str) -> Dict:
        """Get real-time market data"""
        try:
            quote = await self.session.get_live_feed(symbol)
            return {
                'symbol': symbol,
                'price': quote['ltp'],
                'volume': quote['volume'],
                'high': quote['high'],
                'low': quote['low'],
                'timestamp': datetime.fromtimestamp(quote['timestamp']),
                'open': quote['open'],
                'close': quote['close']
            }
        except Exception as e:
            logger.error(f"Error fetching quote for {symbol}: {e}")
            raise