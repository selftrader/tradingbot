import requests
from fastapi import HTTPException
from datetime import datetime
from typing import Optional, Dict, List
from urllib.parse import quote

class DhanClient:
    """
    Dhan API client implementation
    """
    
    BASE_URL = "https://api.dhan.co"  # Production URL
    
    def __init__(self, client_id: str, access_token: str):
        self.client_id = client_id
        self.access_token = access_token
        self.headers = {
            'Accept': 'application/json',
            'client_id': client_id,
            'access-token': access_token,
            'Content-Type': 'application/json'
        }

    async def authenticate(self) -> Dict:
        """
        Generate login URL for Dhan authentication
        """
        try:
            auth_url = (
                f"{self.BASE_URL}/auth/login"
                f"?client_id={quote(self.client_id)}"
                f"&redirect_uri={quote('http://localhost:8000/auth/dhan/callback')}"
            )
            
            print(f"Generated Dhan login URL: {auth_url}")
            return {"login_url": auth_url}
            
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to generate Dhan login URL: {str(e)}"
            )

    async def exchange_token(self, request_token: str) -> str:
        """
        Exchange request token for access token
        """
        try:
            url = f"{self.BASE_URL}/auth/token"
            payload = {
                "client_id": self.client_id,
                "request_token": request_token
            }
            
            response = requests.post(url, headers=self.headers, json=payload)
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Token exchange failed: {response.text}"
                )
                
            data = response.json()
            return data.get("access_token")
            
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to exchange token: {str(e)}"
            )

    async def get_historical_data(
        self,
        security_id: str,
        interval: str,
        from_date: str,
        to_date: str
    ) -> List[Dict]:
        """
        Fetch historical data from Dhan
        
        Parameters:
            security_id: The security identifier
            interval: Time interval (1min, 5min, 15min, 30min, 60min)
            from_date: Start date (YYYY-MM-DD)
            to_date: End date (YYYY-MM-DD)
        """
        try:
            url = f"{self.BASE_URL}/charts/historical"
            
            params = {
                "security_id": security_id,
                "interval": interval,
                "from_date": from_date,
                "to_date": to_date
            }
            
            response = requests.get(url, headers=self.headers, params=params)
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Historical data fetch failed: {response.text}"
                )
                
            data = response.json()
            candles = data.get("data", [])
            
            # Format candle data
            formatted_data = []
            for candle in candles:
                formatted_data.append({
                    'timestamp': candle.get('time'),
                    'open': float(candle.get('open')),
                    'high': float(candle.get('high')),
                    'low': float(candle.get('low')),
                    'close': float(candle.get('close')),
                    'volume': int(candle.get('volume', 0))
                })
                
            return formatted_data
            
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to fetch historical data: {str(e)}"
            )

    async def get_positions(self) -> List[Dict]:
        """Get current positions"""
        try:
            url = f"{self.BASE_URL}/positions"
            response = requests.get(url, headers=self.headers)
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Failed to fetch positions: {response.text}"
                )
                
            return response.json().get("data", [])
            
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to fetch positions: {str(e)}"
            )