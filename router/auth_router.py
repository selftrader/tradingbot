from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr  # ✅ Email validation
from database.connection import get_db
from database.models import User
from passlib.context import CryptContext

auth_router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ✅ Models for Signup & Login
class UserSignup(BaseModel):
    username: str
    email: EmailStr  # ✅ Ensures valid email format
    password: str

class UserLogin(BaseModel):
    email: EmailStr  # ✅ Changed from username to email
    password: str

# ✅ Signup Route
@auth_router.post("/signup")
def signup(user: UserSignup, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = pwd_context.hash(user.password)

    new_user = User(username=user.username, email=user.email, password_hash=hashed_password)
    db.add(new_user)
    db.commit()

    return {"message": "Signup successful."}

# ✅ Updated Login Route to Accept Email
@auth_router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not pwd_context.verify(user.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {"message": "Login successful"}
