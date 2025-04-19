import requests


def get_feed_auth_url(access_token: str) -> str:
    headers = {"Authorization": f"Bearer {access_token}", "Accept": "*/*"}

    url = "https://api.upstox.com/v3/feed/market-data-feed/authorize"
    response = requests.get(url, headers=headers)

    # Debug log to inspect actual response
    print("Auth API Response:", response.status_code, response.text)

    data = response.json()
    if "data" not in data:
        raise Exception(f"❌ Invalid auth response: {data}")

    return data["data"]["authorized_redirect_uri"]
