import asyncio
import ssl
import json
import upstox_client
import websockets
from google.protobuf.json_format import MessageToDict

from services.upstox import MarketDataFeed_pb2 as pb


def get_market_data_feed_authorize(api_version, configuration):
    api_instance = upstox_client.WebsocketApi(
        upstox_client.ApiClient(configuration))
    return api_instance.get_market_data_feed_authorize(api_version)


def decode_protobuf(buffer):
    feed_response = pb.FeedResponse()
    feed_response.ParseFromString(buffer)
    return feed_response


async def fetch_market_data():
    # Create SSL context
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    # ✅ Access token (put yours here)
    access_token = "YOUR_ACCESS_TOKEN"
    configuration = upstox_client.Configuration()
    configuration.access_token = access_token

    api_version = '2.0'
    response = get_market_data_feed_authorize(api_version, configuration)
    ws_url = response.data.authorized_redirect_uri

    # WebSocket connection
    async with websockets.connect(ws_url, ssl=ssl_context) as websocket:
        print("✅ Connected to Upstox WebSocket Feed V3")

        # Build protobuf request (binary)
        subscription_request = pb.FeedRequest()
        subscription_request.guid = "dashboard-stream"
        subscription_request.method = pb.Method.sub
        subscription_request.data.mode = "full"
        subscription_request.data.instrumentKeys.extend([
            "NSE_EQ|INE002A01018"  # RELIANCE instrument key (use actual key from your DB)
        ])

        binary_msg = subscription_request.SerializeToString()

        print("📨 Sending Protobuf Subscription Request...")
        await websocket.send(binary_msg)

        # Listen to feed
        while True:
            message = await websocket.recv()
            if isinstance(message, bytes):
                feed = decode_protobuf(message)
                print(f"📥 Received Feed: {pb.Type.Name(feed.type)}")

                if feed.type == pb.Type.market_info:
                    print("📊 Market Status:")
                    for segment, status in feed.marketInfo.segmentStatus.items():
                        print(f"{segment}: {pb.MarketStatus.Name(status)}")

                elif feed.type == pb.Type.live_feed:
                    for key, data in feed.feeds.items():
                        if data.HasField("ltpc"):
                            print(f"💹 {key} | LTP: ₹{data.ltpc.ltp} | LTQ: {data.ltpc.ltq} | CP: ₹{data.ltpc.cp}")
                        elif data.HasField("fullFeed") and data.fullFeed.HasField("marketFF"):
                            ltp = data.fullFeed.marketFF.ltpc
                            print(f"📈 {key} | FULL LTP: ₹{ltp.ltp} | LTQ: {ltp.ltq} | CP: ₹{ltp.cp}")
            else:
                print("🔔 Non-binary message:", message)


# Run the script
asyncio.run(fetch_market_data())
