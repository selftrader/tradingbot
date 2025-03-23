# websocket/upstox_ws.py

import json
import websocket
import logging
from core.config import ACCESS_TOKEN, WS_URL

# Configure logging
logging.basicConfig(filename="logs/websocket.log", level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

class UpstoxWebSocket:
    def __init__(self):
        self.ws = None

    def on_open(self, ws):
        """Called when the WebSocket connection is opened."""
        print("✅ WebSocket Connection Opened!")

        # Subscribe to NIFTY50 and BANKNIFTY live market data
        subscription_msg = {
            "token": ACCESS_TOKEN,
            "action": "subscribe",
            "params": {
                "mode": "full",  # 'full' for complete data, 'ltp' for LTP only
                "instruments": [
                    "NSE_INDEX|NIFTY50",
                    "NSE_INDEX|BANKNIFTY"
                ]
            }
        }
        ws.send(json.dumps(subscription_msg))
        print("📡 Subscribed to Market Data")

    def on_message(self, ws, message):
        """Called when a message is received from WebSocket."""
        data = json.loads(message)
        print("📊 Live Market Data:", data)
        logging.info(f"Market Data: {data}")

    def on_error(self, ws, error):
        """Called when an error occurs."""
        print(f"❌ WebSocket Error: {error}")
        logging.error(f"WebSocket Error: {error}")

    def on_close(self, ws, close_status_code, close_msg):
        """Called when the WebSocket connection is closed."""
        print("🔴 WebSocket Connection Closed")
        logging.info("WebSocket Connection Closed")

    def connect(self):
        """Connects to the Upstox WebSocket."""
        self.ws = websocket.WebSocketApp(
            WS_URL,
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close
        )
        self.ws.run_forever()

