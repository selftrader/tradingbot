import requests

def get_institutional_activity():
    """Fetch FII/DII money flow data from NSE API."""
    
    url = "https://www.nseindia.com/api/fiidiiTradeReact"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        
        fii_buy = data["data"][-1]["FII_Buy_Value"]
        fii_sell = data["data"][-1]["FII_Sell_Value"]
        dii_buy = data["data"][-1]["DII_Buy_Value"]
        dii_sell = data["data"][-1]["DII_Sell_Value"]

        net_fii = fii_buy - fii_sell
        net_dii = dii_buy - dii_sell

        return {"net_fii": net_fii, "net_dii": net_dii}
    
    except Exception as e:
        return {"error": f"Failed to fetch institutional data: {e}"}
