import requests
from brokers.base_broker import BaseBroker

class UpstoxBroker(BaseBroker):
    """Handles authentication for Upstox"""
    BASE_URL = "https://api.upstox.com"

    def authenticate(self):
        """Authenticate with Upstox API"""
        auth_url = f"{self.BASE_URL}/auth/login"
        headers = {"Content-Type": "application/json"}
        response = requests.post(auth_url, json=self.credentials, headers=headers)

        if response.status_code == 200:
            return response.json()  # ✅ Success
        else:
            raise Exception(f"Authentication failed: {response.text}")  # ❌ Failure
