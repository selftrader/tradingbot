import requests
from brokers.base_broker import BaseBroker

class DhanBroker(BaseBroker):
    """Handles authentication and data retrieval for Dhan"""
    BASE_URL = "https://api.dhan.co/v2"

    def authenticate(self):
        """Authenticate with Dhan API"""
        login_url = f"{self.BASE_URL}/login"
        headers = {"Content-Type": "application/json"}
        response = requests.post(login_url, json=self.credentials, headers=headers)

        if response.status_code == 200:
            return response.json()  # ✅ Success
        else:
            raise Exception(f"Authentication failed: {response.text}")  # ❌ Failure
