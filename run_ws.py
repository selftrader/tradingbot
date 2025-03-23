# run_websocket.py

from services.upstox_ws  import UpstoxWebSocket

if __name__ == "__main__":
    ws_client = UpstoxWebSocket()
    ws_client.connect()
