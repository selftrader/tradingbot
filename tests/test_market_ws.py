import asyncio
import websockets
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def test_market_websocket():
    """Test the market data WebSocket connection."""
    # Replace with actual token and instrument keys
    token = "your_auth_token"
    instrument_keys = ["NSE_INDEX|Nifty 50", "NSE_EQ|RELIANCE"]
    
    uri = f"ws://localhost:8000/ws/market?token={token}"
    
    try:
        async with websockets.connect(uri) as websocket:
            logger.info("Connected to WebSocket server")
            
            # Send subscription message
            subscription = {
                "data": {
                    "instrumentKeys": instrument_keys
                }
            }
            await websocket.send(json.dumps(subscription))
            logger.info(f"Sent subscription for instruments: {instrument_keys}")
            
            # Receive initial connection confirmation
            response = await websocket.recv()
            logger.info(f"Received: {response}")
            
            # Keep connection alive and receive market data
            while True:
                try:
                    # Send ping every 30 seconds
                    await websocket.send("ping")
                    await asyncio.sleep(30)
                    
                    # Receive and process market data
                    data = await websocket.recv()
                    logger.info(f"Received market data: {data}")
                except websockets.exceptions.ConnectionClosed:
                    logger.error("WebSocket connection closed")
                    break
                except Exception as e:
                    logger.error(f"Error: {str(e)}")
                    break
    
    except Exception as e:
        logger.error(f"Failed to connect: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_market_websocket())
