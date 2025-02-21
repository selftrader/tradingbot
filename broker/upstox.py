# brokers/upstox.py
import requests
from config import UPSTOX_API_KEY, UPSTOX_API_SECRET, UPSTOX_REDIRECT_URI

def get_auth_url():
    return (
        f"https://api.upstox.com/v2/oauth/authorize?"
        f"api_key={UPSTOX_API_KEY}&"
        f"redirect_uri={UPSTOX_REDIRECT_URI}&"
        f"response_type=code"
    )

def exchange_code_for_token(auth_code):
    token_url = "https://api.upstox.com/v2/oauth/token"
    payload = {
        'code': auth_code,
        'api_key': UPSTOX_API_KEY,
        'api_secret': UPSTOX_API_SECRET,
        'redirect_uri': UPSTOX_REDIRECT_URI,
        'grant_type': 'authorization_code'
    }
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    response = requests.post(token_url, data=payload, headers=headers)
    return response
