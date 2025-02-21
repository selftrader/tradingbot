from .base_broker import BaseBroker
from kiteconnect import KiteConnect
import logging

logger = logging.getLogger(__name__)

class ZerodhaBroker(BaseBroker):
    def __init__(self, api_key: str, api_secret: str):
        self.api_key = api_key
        self.api_secret = api_secret
        self.kite = KiteConnect(api_key=api_key)
        self.access_token = None

    async def authenticate(self) -> bool:
        try:
            login_url = self.kite.login_url()
            return {"auth_url": login_url, "status": "pending_authorization"}
        except Exception as e:
            logger.error(f"Zerodha authentication error: {e}")
            return False

    async def generate_token(self, request_token: str) -> str:
        try:
            data = self.kite.generate_session(
                request_token,
                api_secret=self.api_secret
            )
            self.access_token = data["access_token"]
            self.kite.set_access_token(self.access_token)
            return self.access_token
        except Exception as e:
            logger.error(f"Zerodha token generation error: {e}")
            raise