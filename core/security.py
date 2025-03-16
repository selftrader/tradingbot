import jwt
import datetime
from core.config import JWT_SECRET, REFRESH_SECRET, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS

# ✅ Generate Access Token
def create_access_token(user_id: int):
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": user_id, "exp": expiration_time}
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")

# ✅ Generate Refresh Token
def create_refresh_token(user_id: int):
    expiration_time = datetime.datetime.utcnow() + datetime.timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    payload = {"sub": user_id, "exp": expiration_time}
    return jwt.encode(payload, REFRESH_SECRET, algorithm="HS256")

# ✅ Decode JWT Token
def verify_token(token: str, secret: str):
    try:
        payload = jwt.decode(token, secret, algorithms=["HS256"])
        return payload.get("sub")  # Returns user_id
    except jwt.ExpiredSignatureError:
        return "expired"
    except jwt.InvalidTokenError:
        return None
