from typing import Dict, List
import logging
from datetime import datetime, timedelta
from .base_broker import BaseBroker
import requests
import json

logger = logging.getLogger(__name__)

class UpstoxBroker(BaseBroker):
    def __init__(self, api_key: str, api_secret: str, redirect_uri: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.redirect_uri = redirect_uri
        self.access_token = None
        self.token_expiry = None
        self.session = None

    async def authenticate(self) -> bool:
        try:
            auth_url = (
                f"https://api.upstox.com/v2/login/authorization/dialog?"
                f"response_type=code&client_id={self.api_key}"
                f"&redirect_uri={self.redirect_uri}"
            )
            return {"auth_url": auth_url, "status": "pending_authorization"}
        except Exception as e:
            logger.error(f"Upstox authentication error: {e}")
            return False

    async def generate_token(self, auth_code: str) -> str:
        try:
            url = "https://api.upstox.com/v2/login/authorization/token"
            data = {
                "code": auth_code,
                "client_id": self.api_key,
                "client_secret": self.api_secret,
                "redirect_uri": self.redirect_uri,
                "grant_type": "authorization_code"
            }
            response = requests.post(url, json=data)
            response.raise_for_status()
            
            token_data = response.json()
            self.access_token = token_data["access_token"]
            # Set token expiry to 24 hours from now
            self.token_expiry = datetime.now() + timedelta(days=1)
            
            return self.access_token
            
        except Exception as e:
            logger.error(f"Upstox token generation error: {e}")
            raise

    async def validate_token(self) -> bool:
        """Validate the current access token"""
        try:
            if not self.access_token or not self.token_expiry:
                return False

            # Check if token is expired or about to expire in next 5 minutes
            if datetime.now() + timedelta(minutes=5) >= self.token_expiry:
                return False

            # Test token validity with a simple API call
            headers = {
                "Authorization": f"Bearer {self.access_token}",
                "Api-Version": "2.0"
            }
            response = requests.get(
                "https://api.upstox.com/v2/user/profile",
                headers=headers
            )
            
            return response.status_code == 200
            
        except Exception as e:
            logger.error(f"Token validation error: {e}")
            return False

    async def refresh_token_if_needed(self) -> bool:
        """Check and refresh token if needed"""
        try:
            if not await self.validate_token():
                # Implement token refresh logic here
                # Note: Upstox might require re-authentication instead of refresh
                logger.info("Token invalid or expired. Re-authentication needed.")
                return False
            return True
            
        except Exception as e:
            logger.error(f"Token refresh error: {e}")
            return False

    async def connect(self) -> bool:
        try:
            self.session = requests.Session(self.api_key)
            await self.session.set_redirect_uri(self.redirect_uri)
            await self.session.set_api_secret(self.api_secret)
            code = await self.session.get_authorization_code()
            await self.session.retrieve_access_token(code)
            logger.info("Successfully connected to Upstox")
            return True
        except Exception as e:
            logger.error(f"Upstox connection error: {str(e)}")
            return False

    async def get_live_quote(self, symbol: str) -> Dict:
        """Get real-time market data from Upstox"""
        try:
            if not self.session:
                raise Exception("Broker not connected")
            
            quote = await self.session.get_live_feed(
                self.session.get_instrument_by_symbol('NSE_EQ', symbol)
            )
            
            return {
                'symbol': symbol,
                'price': quote['ltp'],
                'volume': quote['volume'],
                'high': quote['high'],
                'low': quote['low'],
                'timestamp': datetime.fromtimestamp(quote['timestamp']),
                'change': quote['change'],
                'change_percentage': quote['change_percentage']
            }
        except Exception as e:
            logger.error(f"Error fetching quote for {symbol}: {str(e)}")
            raise

    async def place_order(self, symbol: str, quantity: int, 
                         order_type: str, price: float = None) -> Dict:
        """Place order through Upstox"""
        try:
            if not self.session:
                raise Exception("Broker not connected")
            
            # Get instrument token
            instrument = self.session.get_instrument_by_symbol('NSE_EQ', symbol)
            
            order_params = {
                "instrument": instrument,
                "transaction_type": order_type,
                "quantity": quantity,
                "order_type": "MARKET" if price is None else "LIMIT",
                "product": "I",  # Intraday
                "price": price if price else 0.0,
                "is_amo": False
            }
            
            order = await self.session.place_order(**order_params)
            
            return {
                'order_id': order['order_id'],
                'status': order['status'],
                'symbol': symbol,
                'quantity': quantity,
                'price': price,
                'order_type': order_type,
                'timestamp': datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Order placement error: {str(e)}")
            raise

    async def get_positions(self) -> List[Dict]:
        """Get current positions from Upstox"""
        try:
            if not self.session:
                raise Exception("Broker not connected")
            
            positions = await self.session.get_positions()
            
            return [{
                'symbol': pos['symbol'],
                'quantity': pos['quantity'],
                'average_price': pos['average_price'],
                'last_price': pos['last_price'],
                'pnl': pos['pnl'],
                'product': pos['product'],
                'exchange': pos['exchange']
            } for pos in positions]
        except Exception as e:
            logger.error(f"Error fetching positions: {str(e)}")
            raise