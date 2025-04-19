from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
import requests

ltp_router = APIRouter(prefix="/ltp", tags=["LTP"])

url = "https://api.upstox.com/v2/market-quote/ltp?instrument_key=NSE_EQ%7CINE848E01016,NSE_EQ|INE669E01016"
headers = {"Accept": "application/json", "Authorization": "Bearer {your_access_token}"}

response = requests.get(url, headers=headers)

print(response.text)
