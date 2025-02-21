import requests

class MultiBrokerAPI:
    def __init__(self, broker="zerodha"):
        self.broker = broker.lower()

    def get_live_market_data(self, symbol):
        """Fetches live stock market data from selected broker"""
        if self.broker == "zerodha":
            response = requests.get(f"https://api.kite.trade/quote?symbol={symbol}")
        elif self.broker == "dhan":
            response = requests.get(f"https://api.dhan.co/marketdata/{symbol}")
        else:
            response = requests.get(f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval=5min&apikey=YOUR_API_KEY")

        return response.json() if response.status_code == 200 else None

    def get_options_data(self, symbol):
        """Fetches live F&O (Options) Data"""
        response = requests.get(f"https://api.broker.com/optionsdata/{symbol}")
        return response.json() if response.status_code == 200 else None
    
    def get_live_price(self, symbol):
        """Fetches latest price of a stock or index"""
        response = requests.get(f"https://api.kite.trade/quote?symbol={symbol}")
        return response.json().get("last_price")