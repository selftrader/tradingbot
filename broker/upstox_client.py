import requests
from fastapi import HTTPException
from fastapi.responses import RedirectResponse
from upstox_api.api import Session
from urllib.parse import quote
from config import UPSTOX_REDIRECT_URI, UPSTOX_API_KEY, UPSTOX_API_SECRET
from typing import Optional
from base64 import b64encode
from datetime import datetime
import pytz

def generate_state():
    """Generate a base64 encoded timestamp for state parameter"""
    ist = pytz.timezone('Asia/Kolkata')
    current_time = datetime.now(ist).strftime('%c')
    return b64encode(current_time.encode()).decode()

def authenticate_upstox_v2(client_id: str, redirect_uri: str):
    """
    Creates Upstox login URL and returns URL for frontend to handle redirect
    """
    try:
        # Generate state parameter
        state = generate_state()
        
        # URL encode the redirect URI
        encoded_redirect = quote(redirect_uri, safe='')
        
        # Construct login URL with all required parameters
        login_url = (
            f"https://api.upstox.com/v2/login/authorization/dialog"
            f"?response_type=code"
            f"&client_id={client_id}"
            f"&redirect_uri={encoded_redirect}"
            f"&state={state}"
        )
        
        print(f"Generated Upstox login URL: {login_url}")
        
        # Return URL for frontend to handle
        return {"login_url": login_url}
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate login URL: {str(e)}"
        )

def exchange_code_for_token_v2(authorization_code: str, client_id: str, client_secret: str, redirect_uri: str):
    """
    Exchanges authorization code for access token using exact format from Upstox docs
    """
    try:
        token_url = "https://api.upstox.com/v2/login/authorization/token"
        
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        # Format payload exactly as shown in curl example
        form_data = (
            f'code={authorization_code}'
            f'&client_id={client_id}'
            f'&client_secret={client_secret}'
            f'&redirect_uri={quote(redirect_uri)}'
            f'&grant_type=authorization_code'
        )
        
        print(f"Making token exchange request...")
        print(f"URL: {token_url}")
        print(f"Headers: {headers}")
        print(f"Form data: {form_data}")
        
        response = requests.post(
            url=token_url,
            headers=headers,
            data=form_data
        )
        
        print(f"Response status: {response.status_code}")
        print(f"Response body: {response.text}")
        
        if response.status_code != 200:
            error_msg = "Unknown error"
            try:
                error_data = response.json()
                error_msg = error_data.get('message', str(error_data))
            except:
                error_msg = response.text
            
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Token exchange failed: {error_msg}"
            )
        
        token_data = response.json()
        access_token = token_data.get("access_token")
        
        if not access_token:
            raise HTTPException(
                status_code=400,
                detail="No access token in response"
            )
        
        print("Successfully received access token")
        return access_token
        
    except HTTPException as he:
        raise he
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to exchange code for token: {str(e)}"
        )

def get_historical_data(access_token: str, instrument_key: str, interval: str, from_date: str, to_date: str):
    """
    Fetch historical data from Upstox using the access token
    
    Parameters:
        access_token: The token received from auth
        instrument_key: The instrument identifier (eg: 'NSE_EQ|INE001A01036')
        interval: Time interval ('1minute', '5minute', 'day', etc.)
        from_date: Start date in format YYYY-MM-DD
        to_date: End date in format YYYY-MM-DD
    """
    try:
        url = "https://api.upstox.com/v2/historical-candle/intraday"
        
        headers = {
            'accept': 'application/json',
            'Api-Version': '2.0',
            'Authorization': f'Bearer {access_token}'
        }
        
        params = {
            'instrument_key': instrument_key,
            'interval': interval,
            'from': from_date,
            'to': to_date
        }
        
        print(f"Fetching historical data...")
        print(f"URL: {url}")
        print(f"Params: {params}")
        
        response = requests.get(
            url=url,
            headers=headers,
            params=params
        )
        
        if response.status_code != 200:
            error_msg = "Unknown error"
            try:
                error_data = response.json()
                error_msg = error_data.get('message', str(error_data))
            except:
                error_msg = response.text
            
            raise HTTPException(
                status_code=response.status_code,
                detail=f"Historical data fetch failed: {error_msg}"
            )
        
        data = response.json()
        candles = data.get('data', {}).get('candles', [])
        
        if not candles:
            print("No historical data found")
            return []
            
        # Convert data to more usable format
        formatted_data = []
        for candle in candles:
            if len(candle) >= 6:  # OHLCV format
                formatted_data.append({
                    'timestamp': candle[0],
                    'open': candle[1],
                    'high': candle[2],
                    'low': candle[3],
                    'close': candle[4],
                    'volume': candle[5]
                })
        
        print(f"Successfully fetched {len(formatted_data)} candles")
        return formatted_data
        
    except HTTPException as he:
        raise he
    except Exception as e:
        print(f"Unexpected error fetching historical data: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch historical data: {str(e)}"
        )