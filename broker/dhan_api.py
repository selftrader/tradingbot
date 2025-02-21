# broker/dhan_api.py

import requests
import logging
from .base_broker import BaseBroker

class BrokerDhan(BaseBroker):
    def __init__(self, config):
        self.api_key = config.get('API_KEY')
        self.api_secret = config.get('API_SECRET')
        self.access_token = config.get('ACCESS_TOKEN')
        self.base_url = config.get('BASE_URL')
        self.symbol = config.get('symbol')
        self.exchange = config.get('exchange', 'NSE')
        self.trade_amount = config.get('trade_amount')
        # Setup headers for authentication.
        self.headers = {
            'Authorization': f"Bearer {self.access_token}",
            'X-API-KEY': self.api_key
        }
        logging.info("Initialized DHAN broker client.")

    def place_order(self, order_type, price=None):
        order_side = "BUY" if order_type.upper() == "BUY" else "SELL"
        payload = {
            'symbol': self.symbol,
            'exchange': self.exchange,
            'transaction_type': order_side,
            'quantity': self.trade_amount,
            'order_type': 'MARKET' if price is None else 'LIMIT',
            'price': price
        }
        try:
            url = f"{self.base_url}/order/place"
            response = requests.post(url, headers=self.headers, json=payload)
            response_data = response.json()
            if response.status_code == 200 and response_data.get('status') == 'success':
                order_id = response_data.get('order_id')
                logging.info(f"DHAN: Placed {order_type} order. Order ID: {order_id}")
                return order_id
            else:
                error_message = response_data.get('error', 'Unknown error')
                logging.error(f"DHAN order placement failed: {error_message}")
                raise Exception(error_message)
        except Exception as e:
            logging.error(f"DHAN order placement exception: {e}")
            raise e
