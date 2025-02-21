from typing import Dict
import os
from dotenv import load_dotenv

def get_config() -> Dict:
    load_dotenv()
    
    return {
        # Broker Selection
        "BROKER_NAME": os.getenv("BROKER_NAME", "upstox"),
        
        # Upstox Credentials
        "UPSTOX_API_KEY": os.getenv("UPSTOX_API_KEY"),
        "UPSTOX_API_SECRET": os.getenv("UPSTOX_API_SECRET"),
        "UPSTOX_REDIRECT_URI": os.getenv("UPSTOX_REDIRECT_URI"),
        
        # Zerodha Credentials
        "ZERODHA_API_KEY": os.getenv("ZERODHA_API_KEY"),
        "ZERODHA_API_SECRET": os.getenv("ZERODHA_API_SECRET"),
        
        # Trading Parameters
        "SYMBOL": os.getenv("TRADING_SYMBOL"),
        "QUANTITY": int(os.getenv("TRADING_QUANTITY", "1")),
        "RISK_PER_TRADE": float(os.getenv("RISK_PER_TRADE", "0.01"))
    }

def get_options_config() -> Dict:
    load_dotenv()
    return {
        "TRADING_TYPE": "OPTIONS",
        "INDEX": os.getenv("OPTIONS_INDEX", "NIFTY"),  # NIFTY or BANKNIFTY
        "OPTION_TYPE": os.getenv("OPTION_TYPE", "CE"),  # CE or PE
        "STRIKE_OFFSET": int(os.getenv("STRIKE_OFFSET", "0")),  # ATM +/- offset
        "EXPIRY_SELECTION": os.getenv("EXPIRY_SELECTION", "WEEKLY"),  # WEEKLY/MONTHLY
        "LOT_SIZE": int(os.getenv("LOT_SIZE", "50")),
        "MAX_LOTS": int(os.getenv("MAX_LOTS", "2")),
        "RISK_PER_TRADE": float(os.getenv("RISK_PER_TRADE", "0.01"))
    }

# config.py
UPSTOX_API_KEY = 'YOUR_UPSTOX_API_KEY'
UPSTOX_API_SECRET = 'YOUR_UPSTOX_API_SECRET'
UPSTOX_REDIRECT_URI = 'http://localhost:8000/auth/upstox/callback'  # Example redirect URI

# Dhan API access token
DHAN_ACCESS_TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJpc3MiOiJkaGFuIiwicGFydG5lcklkIjoiIiwiZXhwIjoxNzM5NzY3Mzc0LCJ0b2tlbkNvbnN1bWVyVHlwZSI6IlNFTEYiLCJ3ZWJob29rVXJsIjoiaHR0cDovL2xvY2FsaG9zdDo4MDAwL2F1dGgvZGhhbi9jYWxsYmFjayIsImRoYW5DbGllbnRJZCI6IjExMDU3MDA1NjgifQ.kVcjwGo0hV22udd6qPkh8q6NDwaXm3bISVEzfNvGGxKJcpgAHTChpnaII6sLx4M9tGMrorU-TRkaJt6dhTGPbQ'
DHAN_REDIRECT_URI = 'http://localhost:8000/auth/dhan/callback'  # Example redirect URI


# Zerodha configuration (example placeholders)
ZERODHA_API_KEY = 'YOUR_ZERODHA_API_KEY'
ZERODHA_API_SECRET = 'YOUR_ZERODHA_API_SECRET'
ZERODHA_REDIRECT_URI = 'http://localhost:5000/auth/zerodha/callback'
# Multi-broker configuration: currently only DHAN is implemented.
BROKER_CONFIG = {
    'brokers': [
        {
            'name': 'Dhan',
            'API_KEY': 'YOUR_DHAN_API_KEY',
            'API_SECRET': 'YOUR_DHAN_API_SECRET',
            'ACCESS_TOKEN': 'YOUR_DHAN_ACCESS_TOKEN',
            'BASE_URL': 'https://api.dhan.com/v1',  # Hypothetical endpoint; replace with real one.
            'symbol': 'RELIANCE',
            'exchange': 'NSE',
            'trade_amount': 1
        }
    ]
}

# Additional trading configuration parameters
TRADING_CONFIG = {
    'analysis_interval': 60,   # seconds between each analysis/trading cycle
    'learning_interval': 3600  # seconds between model updates (if using scheduled learning)
}

# Data configuration: path to historical market data.
DATA_CONFIG = {
    'data_file': 'data/sample_data.csv'
}

# AI Predictor configuration: location of the production‑trained model.
PREDICTOR_CONFIG = {
    'model_path': 'models/production_model.pkl',  # Ensure this file exists; otherwise, train your model.
    'use_dummy': False  # Must be False in production!
}

# Logging configuration
LOGGING_CONFIG = {
    'log_file': 'logs/bot.log',
    'log_level': 'INFO'
}



# config.py - Stores sectoral indices and their constituent stocks

# Dictionary of sectoral indices and their F&O tradable constituent stocks
SECTORAL_INDICES = {
    "NIFTY Auto": ["ASHOKLEY.NS", "BAJAJ-AUTO.NS", "EICHERMOT.NS", "HEROMOTOCO.NS", "M&M.NS", "MARUTI.NS", "TATAMOTORS.NS", "TVSMOTOR.NS"],
    "NIFTY Bank": ["AXISBANK.NS", "BANDHANBNK.NS", "HDFCBANK.NS", "ICICIBANK.NS", "INDUSINDBK.NS", "KOTAKBANK.NS", "PNB.NS", "SBIN.NS"],
    "NIFTY Financial Services": ["BAJFINANCE.NS", "BAJAJFINSV.NS", "HDFC.NS", "HDFCBANK.NS", "ICICIBANK.NS", "KOTAKBANK.NS", "SBIN.NS"],
    "NIFTY FMCG": ["BRITANNIA.NS", "COLPAL.NS", "DABUR.NS", "GODREJCP.NS", "HINDUNILVR.NS", "ITC.NS", "MARICO.NS", "NESTLEIND.NS", "TATACONSUM.NS", "UBL.NS"],
    "NIFTY IT": ["HCLTECH.NS", "INFY.NS", "TCS.NS", "TECHM.NS", "WIPRO.NS"],
    "NIFTY Media": ["PVR.NS", "SUNTV.NS", "ZEEL.NS"],
    "NIFTY Metal": ["COALINDIA.NS", "HINDALCO.NS", "JSWSTEEL.NS", "NATIONALUM.NS", "SAIL.NS", "TATASTEEL.NS", "VEDL.NS"],
    "NIFTY Pharma": ["AUROPHARMA.NS", "CIPLA.NS", "DIVISLAB.NS", "DRREDDY.NS", "LUPIN.NS", "SUNPHARMA.NS", "TORNTPHARM.NS"],
    "NIFTY Private Bank": ["AXISBANK.NS", "HDFCBANK.NS", "ICICIBANK.NS", "INDUSINDBK.NS", "KOTAKBANK.NS"],
    "NIFTY PSU Bank": ["BANKBARODA.NS", "PNB.NS", "SBIN.NS"],
    "NIFTY Realty": ["DLF.NS", "GODREJPROP.NS"],
    "NIFTY Oil & Gas": ["BPCL.NS", "GAIL.NS", "HINDPETRO.NS", "IOC.NS", "ONGC.NS", "RELIANCE.NS"]
}
