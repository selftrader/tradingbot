from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from jose import JWTError
from sqlalchemy.orm import Session
from passlib.context import CryptContext
import jwt
import os
from core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from database.connection import get_db
from database.models import User
from fastapi.security import OAuth2PasswordBearer

from router.broker_router import SECRET_KEY

ALGORITHM = "HS256"
REFRESH_SECRET = os.getenv("REFRESH_SECRET", "your-refresh-secret-key")
SECRET_KEY = os.getenv("JWT_SECRET", "your-access-secret-key")
ACCESS_TOKEN_EXPIRE_MINUTES = 15  # Access Token valid for 15 minutes
REFRESH_TOKEN_EXPIRE_DAYS = 7  # ✅ Refresh Token valid for 7 days

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user_data):
        hashed_password = pwd_context.hash(user_data.password)
        new_user = User(username=user_data.username, email=user_data.email, password=hashed_password)
        self.db.add(new_user)
        self.db.commit()
        self.db.refresh(new_user)
        return {"message": "User created successfully"}

    def authenticate_user(self, user_data):
        user = self.db.query(User).filter(User.email == user_data.email).first()
        if not user or not pwd_context.verify(user_data.password, user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        access_token = self.create_access_token(user.username)
        refresh_token = self.create_refresh_token(user.username)  # ✅ Define refreshToken
        return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

    def create_access_token(self, username: str):
        expiration = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        token_data = {"sub": username, "exp": expiration}
        return jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)

    def create_refresh_token(self, username: str):
        expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        token_data = {"sub": username, "exp": expire}
        return jwt.encode(token_data, REFRESH_SECRET, algorithm=ALGORITHM)


# ✅ Add `get_current_user` function
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    """
    Extract user from JWT token.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.email == email).first()
    if user is None:
        raise credentials_exception

    return user




def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password: str):
    return pwd_context.hash(password)


def create_access_token(email: str):
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": email, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

# ✅ Function to Create Refresh Token
def create_refresh_token(email: str):
    expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    payload = {"sub": email, "exp": expire}
    return jwt.encode(payload, REFRESH_SECRET, algorithm=ALGORITHM)

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Access token expired. Please refresh.")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")