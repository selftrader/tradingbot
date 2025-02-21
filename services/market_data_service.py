import aiohttp
import pandas as pd
from typing import Dict, List
import logging

logger = logging.getLogger(__name__)

class MarketDataService:
    def __init__(self):
        self.session = None

    async def _ensure_session(self):
        if not self.session:
            self.session = aiohttp.ClientSession()

    async def fetch_options_chain(self, symbol: str) -> Dict:
        """Fetch options chain data"""
        await self._ensure_session()
        try:
            async with self.session.get(f"/api/options/{symbol}") as response:
                return await response.json()
        except Exception as e:
            logger.error(f"Error fetching options chain: {e}")
            return {}

    async def fetch_fii_dii_data(self) -> Dict:
        """Fetch FII/DII data"""
        await self._ensure_session()
        try:
            async with self.session.get("/api/market/fii-dii") as response:
                return await response.json()
        except Exception as e:
            logger.error(f"Error fetching FII/DII data: {e}")
            return {}

    async def close(self):
        """Close the session"""
        if self.session:
            await self.session.close()
            self.session = None