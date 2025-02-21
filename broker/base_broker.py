# brokers/base.py

class BrokerBase:
    def get_auth_url(self):
        raise NotImplementedError("Subclasses must implement this method.")

    def exchange_code_for_token(self, auth_code):
        raise NotImplementedError("Subclasses must implement this method.")
