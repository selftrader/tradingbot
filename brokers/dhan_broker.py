from brokers.base_broker import BaseBroker
import aiohttp

class DhanBroker(BaseBroker):
    def __init__(self, api_key: str, client_id: str):
        self.api_key = api_key
        self.client_id = client_id
        self.base_url = "https://api.dhan.co"

    async def authenticate(self) -> bool:
        """Dhan API does not require authentication, just API key"""
        return True

    async def get_tradeable_symbols(self):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{self.base_url}/market/instruments") as response:
                return await response.json()

    async def place_order(self, symbol: str, quantity: int, side: str, order_type: str):
        """Place a trade on Dhan"""
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.base_url}/orders", json={
                "symbol": symbol,
                "quantity": quantity,
                "side": side,
                "order_type": order_type,
                "exchange": "NSE"
            }, headers={"X-API-KEY": self.api_key}) as response:
                return await response.json()
