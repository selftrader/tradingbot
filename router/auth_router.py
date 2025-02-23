from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from database.connection import get_db
from database.models import User
import jwt
import datetime
import os
from passlib.context import CryptContext

SECRET_KEY = os.getenv("JWT_SECRET", "mysecretkey")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

auth_router = APIRouter()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Request models
class UserSignup(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

# Signup route
@auth_router.post("/signup")
def signup(user: UserSignup, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_password = pwd_context.hash(user.password)
    new_user = User(username=user.username, email=user.email, password_hash=hashed_password)
    db.add(new_user)
    db.commit()
    return {"message": "User registered successfully"}

# Login route
@auth_router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    try:
        db_user = db.query(User).filter(User.username == user.username).first()

        # ✅ Ensure user exists
        if not db_user:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        # ✅ Ensure password matches
        if not pwd_context.verify(user.password, db_user.password_hash):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        # ✅ Generate JWT token
        token = jwt.encode(
            {"sub": db_user.username, "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)},
            SECRET_KEY,
            algorithm=ALGORITHM
        )

        return {"access_token": token, "token_type": "bearer"}

    except Exception as e:
        print(f"⚠️ Login Error: {e}")  # ✅ Logs error for debugging
        raise HTTPException(status_code=500, detail="Internal server error")