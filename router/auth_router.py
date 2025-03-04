import datetime
from fastapi import APIRouter, Depends, HTTPException
import jwt
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr  # ✅ Email validation
from database.connection import get_db
from database.models import User
from passlib.context import CryptContext

# ✅ Import SECRET_KEY from `auth_service` (NOT `broker_router`)
from services.auth_service import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM

auth_router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ✅ Models for Signup & Login
class UserSignup(BaseModel):
    username: str
    email: EmailStr  # ✅ Ensures valid email format
    password: str

class UserLogin(BaseModel):
    email: EmailStr  # ✅ Login using email
    password: str

# ✅ Generate JWT Token
def create_access_token(username: str):
    expiration = datetime.datetime.utcnow() + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token_data = {"sub": username, "exp": expiration}
    return jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)

# ✅ Signup Route
@auth_router.post("/signup")
def signup(user: UserSignup, db: Session = Depends(get_db)):
    """Registers a new user and returns a JWT token."""
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = pwd_context.hash(user.password)

    # ✅ Ensure password is stored in `password_hash`
    new_user = User(username=user.username, email=user.email, password_hash=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # ✅ Generate token for immediate login
    token = create_access_token(new_user.username)

    return {"message": "Signup successful", "access_token": token, "token_type": "bearer"}

# ✅ Updated Login Route to Accept Email
@auth_router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    """Authenticates user and returns a JWT token."""
    db_user = db.query(User).filter(User.email == user.email).first()

    # ✅ Fix: Use `password_hash` instead of `password`
    if not db_user or not pwd_context.verify(user.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # ✅ Generate token after successful login
    token = create_access_token(db_user.username)

    return {"message": "Login successful", "access_token": token, "token_type": "bearer"}
