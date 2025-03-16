import requests
from brokers.base_broker import BaseBroker

class ZerodhaBroker(BaseBroker):
    """Handles authentication for Zerodha"""
    BASE_URL = "https://api.kite.trade"

    def authenticate(self):
        """Authenticate with Zerodha API"""
        session_url = f"{self.BASE_URL}/session/token"
        headers = {"X-Kite-Version": "3", "Content-Type": "application/json"}
        response = requests.post(session_url, json=self.credentials, headers=headers)

        if response.status_code == 200:
            return response.json()  # ✅ Success
        else:
            raise Exception(f"Authentication failed: {response.text}")  # ❌ Failure
