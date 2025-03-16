from fastapi import Request, HTTPException
import jwt
import os
from datetime import datetime, timedelta
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

# ✅ Load Secret Keys
SECRET_KEY = os.getenv("JWT_SECRET", "mysecretkey")
REFRESH_SECRET = os.getenv("REFRESH_SECRET", "refreshsecretkey")
ALGORITHM = "HS256"

# ✅ Token Expiry Times
ACCESS_TOKEN_EXPIRY_MINUTES = 15  # 15 min expiry for access token
REFRESH_TOKEN_EXPIRY_DAYS = 7     # 7-day expiry for refresh token

def create_access_token(data: dict, expires_delta: timedelta = None):
    """Creates a new access token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRY_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

class TokenRefreshMiddleware(BaseHTTPMiddleware):
    """Middleware to detect expired tokens and refresh them if possible"""

    async def dispatch(self, request: Request, call_next):
        access_token = request.headers.get("Authorization")
        refresh_token = request.headers.get("Refresh-Token")  # ✅ Look for refresh token

        if access_token and "Bearer" in access_token:
            access_token = access_token.split("Bearer ")[-1]
            try:
                jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
            except jwt.ExpiredSignatureError:
                # ✅ If access token is expired, check refresh token
                if not refresh_token:
                    return JSONResponse(status_code=401, content={"detail": "Token expired. No refresh token provided."})

                try:
                    decoded_refresh = jwt.decode(refresh_token, REFRESH_SECRET, algorithms=[ALGORITHM])
                    user_email = decoded_refresh.get("sub")  # Assuming 'sub' stores email/ID

                    # ✅ Issue a new access token
                    new_access_token = create_access_token({"sub": user_email})

                    return JSONResponse(
                        status_code=401,
                        content={"detail": "Token expired. Refreshed successfully.", "new_access_token": new_access_token}
                    )
                
                except jwt.ExpiredSignatureError:
                    return JSONResponse(status_code=401, content={"detail": "Refresh token expired. Please log in again."})
                except jwt.InvalidTokenError:
                    return JSONResponse(status_code=401, content={"detail": "Invalid refresh token. Please log in again."})

            except jwt.InvalidTokenError:
                return JSONResponse(status_code=401, content={"detail": "Invalid token. Please log in again."})

        response = await call_next(request)
        return response
