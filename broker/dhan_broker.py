from dhanhq import dhan
from brokers.base_broker import BaseBroker
import os

class DhanBroker(BaseBroker):
    def __init__(self, client_id: str, access_token: str):
        self.client_id = client_id
        self.access_token = access_token
        self.dhan_client = dhan.Dhan(client_id, access_token)

    def authenticate(self) -> str:
        """DhanHQ uses API key and access token for authentication"""
        if not self.access_token:
            raise ValueError("Access token is required for DhanHQ authentication")
        return self.access_token

    def get_market_data(self, symbol: str) -> dict:
        """Fetch market data for a given symbol from DhanHQ"""
        try:
            market_data = self.dhan_client.get_quotes(symbol)
            return market_data
        except Exception as e:
            raise ValueError(f"Failed to fetch market data: {str(e)}")

    def place_order(self, symbol: str, quantity: int, transaction_type: str, order_type: str, price: float = None) -> dict:
        """Place an order via DhanHQ"""
        try:
            order_response = self.dhan_client.place_order(
                security_id=symbol,
                transaction_type=transaction_type,
                quantity=quantity,
                order_type=order_type,
                price=price
            )
            return order_response
        except Exception as e:
            raise ValueError(f"Order placement failed: {str(e)}")

    def get_positions(self) -> list:
        """Fetch open positions"""
        try:
            positions = self.dhan_client.get_positions()
            return positions
        except Exception as e:
            raise ValueError(f"Failed to fetch positions: {str(e)}")

    def get_historical_data(self, symbol: str, interval: str, start_date: str, end_date: str) -> dict:
        """Fetch historical data"""
        try:
            historical_data = self.dhan_client.get_candle_data(symbol, interval, start_date, end_date)
            return historical_data
        except Exception as e:
            raise ValueError(f"Failed to fetch historical data: {str(e)}")
