# import os
# import json
# import redis
# from datetime import timedelta

# redis_client = redis.Redis.from_url(os.getenv("REDIS_URL"), decode_responses=True)

# def store_temp_upstox_credentials(user_id: int, api_key: str, api_secret: str):
#     key = f"upstox:auth:{user_id}"
#     value = json.dumps({
#         "api_key": api_key,
#         "api_secret": api_secret
#     })
#     redis_client.setex(key, timedelta(minutes=10), value)  # 10-minute TTL

# def get_temp_upstox_credentials(user_id: int):
#     key = f"upstox:auth:{user_id}"
#     data = redis_client.get(key)
#     if data:
#         return json.loads(data)
#     return None

# def delete_temp_upstox_credentials(user_id: int):
#     key = f"upstox:auth:{user_id}"
#     redis_client.delete(key)
