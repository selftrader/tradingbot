from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
import jwt
import datetime
import os

from database.models import User

SECRET_KEY = os.getenv("JWT_SECRET", "mysecretkey")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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
        user = self.db.query(User).filter(User.username == user_data.username).first()
        if not user or not pwd_context.verify(user_data.password, user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        token = self.create_access_token(user.username)
        return {"access_token": token, "token_type": "bearer"}

    def create_access_token(self, username: str):
        expiration = datetime.datetime.utcnow() + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        token_data = {"sub": username, "exp": expiration}
        return jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
