class BaseBroker:
    """Base class for broker authentication and API calls"""
    def __init__(self, broker_name: str, credentials: dict):
        self.broker_name = broker_name
        self.credentials = credentials

    def authenticate(self):
        """Authenticate with the broker's API"""
        raise NotImplementedError("Authentication must be implemented in subclasses.")

    def fetch_account_data(self):
        """Fetch user account details from broker"""
        raise NotImplementedError("Fetching account data must be implemented in subclasses.")
