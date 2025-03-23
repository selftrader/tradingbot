import requests

def get_options_chain(symbol: str):
    """Fetch live options chain data from NSE."""
    
    url = f"https://www.nseindia.com/api/option-chain-equities?symbol={symbol}"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        return data["records"]["data"]
    
    except Exception as e:
        return {"error": f"Failed to fetch options chain: {e}"}
