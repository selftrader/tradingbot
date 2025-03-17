from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
import jwt
import os

# ✅ Load Secret Keys
SECRET_KEY = os.getenv("JWT_SECRET", "your-access-secret-key")
ALGORITHM = "HS256"
ALLOWED_ORIGIN = "http://localhost:3000"  # ✅ Change this to your frontend URL

class TokenRefreshMiddleware(BaseHTTPMiddleware):
    """Middleware to detect expired tokens and refresh them if possible"""

    async def dispatch(self, request: Request, call_next):
        if request.method == "OPTIONS":  # ✅ Handle preflight CORS requests
            response = JSONResponse(status_code=200, content={})
            response.headers["Access-Control-Allow-Origin"] = ALLOWED_ORIGIN
            response.headers["Access-Control-Allow-Credentials"] = "true"
            response.headers["Access-Control-Allow-Headers"] = "Authorization, Content-Type"
            response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
            return response

        access_token = request.headers.get("Authorization")

        if access_token and "Bearer" in access_token:
            access_token = access_token.split("Bearer ")[-1]
            try:
                jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
            except jwt.ExpiredSignatureError:
                response = JSONResponse(
                    status_code=401,
                    content={"detail": "Access token expired", "code": "token_expired"},
                )
                response.headers["Access-Control-Allow-Origin"] = ALLOWED_ORIGIN
                response.headers["Access-Control-Allow-Credentials"] = "true"
                response.headers["Access-Control-Allow-Headers"] = "Authorization, Content-Type"
                response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE"
                return response
            except jwt.PyJWTError:  # ✅ FIX: Use correct error type
                response = JSONResponse(
                    status_code=401,
                    content={"detail": "Invalid token"},
                )
                response.headers["Access-Control-Allow-Origin"] = ALLOWED_ORIGIN
                return response

        response = await call_next(request)
        return response
