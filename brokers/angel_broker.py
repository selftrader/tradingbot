import requests
from brokers.base_broker import BaseBroker

class AngelBroker(BaseBroker):
    """Handles authentication for Angel One"""
    BASE_URL = "https://api.angelbroking.com"

    def authenticate(self):
        """Authenticate with Angel One API"""
        login_url = f"{self.BASE_URL}/rest/authenticate"
        headers = {"Content-Type": "application/json"}
        response = requests.post(login_url, json=self.credentials, headers=headers)

        if response.status_code == 200:
            return response.json()  # ✅ Success
        else:
            raise Exception(f"Authentication failed: {response.text}")  # ❌ Failure
