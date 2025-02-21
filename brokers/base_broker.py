from abc import ABC, abstractmethod
from typing import Dict, Optional, List
import logging
import aiohttp

logger = logging.getLogger(__name__)

class BaseBroker(ABC):
    @abstractmethod
    async def authenticate(self) -> bool:
        """Authenticate with the broker"""
        pass

    @abstractmethod
    async def generate_token(self, auth_code: str) -> str:
        """Generate/refresh access token"""
        pass

    @abstractmethod
    async def validate_token(self) -> bool:
        """Validate current token"""
        pass

    @property
    def is_authenticated(self) -> bool:
        """Check if broker is authenticated"""
        return bool(self.access_token and self.token_expiry)

class DhanBroker(BaseBroker):
    def __init__(self, api_key: str, client_id: str):
        self.api_key = api_key
        self.client_id = client_id
        self.base_url = "https://api.dhan.co"

    async def get_tradeable_symbols(self) -> List[Dict]:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}/instruments") as response:
                data = await response.json()
                return [
                    {
                        "symbol": item["symbol"],
                        "name": item["tradingName"],
                        "segment": item["exchange"],
                        "lastPrice": item.get("lastPrice")
                    }
                    for item in data
                ]

    async def get_market_data(self, symbol: str) -> Dict:
        # Implement market data fetching
        pass

class UpstoxBroker(BaseBroker):
    def __init__(self, api_key: str, secret_key: str):
        self.api_key = api_key
        self.secret_key = secret_key
        self.base_url = "https://api.upstox.com/v2"

    async def get_tradeable_symbols(self) -> List[Dict]:
        # Implement Upstox-specific symbols fetching
        return [
            {"symbol": "NIFTY", "name": "Nifty 50", "segment": "INDEX"},
            {"symbol": "RELIANCE", "name": "Reliance Industries", "segment": "NSE"}
        ]

    async def get_market_data(self, symbol: str) -> Dict:
        # Implement market data fetching
        pass