import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Secret Keys for JWT Tokens
JWT_SECRET = os.getenv("JWT_SECRET", "default_secret_key")
REFRESH_SECRET = os.getenv("REFRESH_SECRET", JWT_SECRET)

# Token Expiry Settings
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7
