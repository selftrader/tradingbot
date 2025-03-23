import asyncio
import websockets
import json

DHAN_WEBSOCKET_URL = "wss://api-feed.dhan.co?version=2&token=YOUR_ACCESS_TOKEN"

async def subscribe_to_live_feed(symbol):
    """Subscribe to Dhan's live market feed."""
    async with websockets.connect(DHAN_WEBSOCKET_URL) as websocket:
        subscription_message = {
            "RequestCode": 15,
            "InstrumentCount": 1,
            "InstrumentList": [{"ExchangeSegment": "NSE_EQ", "SecurityId": symbol}]
        }
        
        await websocket.send(json.dumps(subscription_message))
        while True:
            response = await websocket.recv()
            print(f"📊 Live Update: {response}")

async def main():
    await subscribe_to_live_feed("1333")  # Replace with actual Security ID

if __name__ == "__main__":
    asyncio.run(main())
