import os
import requests
from urllib.parse import urlencode
from datetime import datetime, timedelta
from fastapi import HTTPException
from database.models import BrokerConfig

UPSTOX_BASE_URL = "https://api.upstox.com/v2"
UPSTOX_AUTH_BASE_URL = "https://api.upstox.com/v2/login/authorization/dialog"
UPSTOX_TOKEN_URL = "https://api.upstox.com/v2/login/authorization/token"
UPSTOX_REDIRECT_URI = os.getenv("UPSTOX_REDIRECT_URI")


def generate_upstox_auth_url(api_key: str) -> str:
    """Generate Upstox OAuth URL for user redirection."""
    query = {
        "client_id": api_key,
        "redirect_uri": UPSTOX_REDIRECT_URI,
        "response_type": "code",
        "scope": "read,trade",
    }
    return f"{UPSTOX_AUTH_BASE_URL}?{urlencode(query)}"


def exchange_upstox_token(code: str, api_key: str, api_secret: str) -> dict:
    """Exchange authorization code for access token."""
    payload = {
        "code": code,
        "client_id": api_key,
        "client_secret": api_secret,
        "redirect_uri": UPSTOX_REDIRECT_URI,
        "grant_type": "authorization_code",
    }

    response = requests.post(UPSTOX_TOKEN_URL, data=payload)
    if response.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to exchange Upstox code")

    data = response.json()["data"]
    return {
        "access_token": data["access_token"],
        "refresh_token": data.get("refresh_token"),
        "expires_in": data.get("expires_in"),  # seconds
        "user_id": data.get("user_id"),
        "client_id": data.get("client_id"),
    }


def generate_upstox_auth_url(api_key: str,user_id: int) -> str:
    params = {
        "response_type": "code",
        "client_id": api_key,
        "redirect_uri": UPSTOX_REDIRECT_URI,
        "state": str(user_id),
    }
    return f"{UPSTOX_BASE_URL}/login/authorization/dialog?{urlencode(params)}"

def exchange_code_for_token(code: str,api_key: str, api_secret: str):
    url = f"{UPSTOX_BASE_URL}/login/authorization/token"
    payload = {
        "code": code,
        "client_id": api_key,
        "client_secret": api_secret,
        "redirect_uri": UPSTOX_REDIRECT_URI,
        "grant_type": "authorization_code"
    }

    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    response = requests.post(url, data=payload, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Token exchange failed: {response.text}")
    return response.json()