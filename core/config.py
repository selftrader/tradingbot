import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Secret Keys for JWT Tokens
JWT_SECRET = os.getenv("JWT_SECRET", "your-access-secret-key")
REFRESH_SECRET = os.getenv("REFRESH_SECRET", JWT_SECRET)

# Token Expiry Settings
ACCESS_TOKEN_EXPIRE_MINUTES = 36000  # 10 hour
REFRESH_TOKEN_EXPIRE_DAYS = 7

TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID"  # User ID or Group ID

# TODO - Add more config variables here
# ✅ 1. Set Up Telegram Bot
# Go to Telegram and search for @BotFather.
# Type /newbot and follow the instructions.
# Copy the bot token and store it in config.py.



# ✅ 2. Get Chat ID
# Search for your bot on Telegram and send a message.

EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USERNAME = "your-email@gmail.com"
EMAIL_PASSWORD = "your-email-password"

TWILIO_ACCOUNT_SID = "your-twilio-sid"
TWILIO_AUTH_TOKEN = "your-twilio-auth-token"
TWILIO_PHONE_NUMBER = "+123456789"



# Upstox API Configuration

API_KEY = "your_api_key"
API_SECRET = "your_api_secret"
REDIRECT_URI = "your_redirect_uri"
ACCESS_TOKEN = "your_access_token"  # You need to generate this
WS_URL = "wss://api.upstox.com/live/market-data"  # Upstox WebSocket URL

