from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException, status
import logging
import jwt
from sqlalchemy.orm import Session
from database.schemas import UserEmailLogin, UserSignup, OTPVerification, UserResponse, AuthResponse, OTPResponse
from pydantic import BaseModel, EmailStr  # ✅ Email validation
from database.connection import get_db
from database.models import OTP, User
from passlib.context import CryptContext
from services.otp_service import generate_otp, send_otp_twilio, store_otp

# Function to hash passwords
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# ✅ Import SECRET_KEY from `auth_service` (NOT `broker_router`)
from services.auth_service import SECRET_KEY, ACCESS_TOKEN_EXPIRE_MINUTES, ALGORITHM, verify_password

auth_router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#  Generate JWT Token
def create_access_token(email: str):
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)  # ✅ Fix here
    payload = {"sub": email, "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

# ✅ Signup Route
@auth_router.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(user: UserSignup, db: Session = Depends(get_db)):
    """Registers a new user and sends OTP via SMS for verification."""
    existing_user = db.query(User).filter(
        (User.email == user.email) | (User.phone_number == user.phone_number)
    ).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    existing_phone = db.query(User).filter(User.phone_number == user.phone_number).first()
    if existing_phone:
        raise HTTPException(status_code=400, detail="Phone number already registered")

    otp_code = generate_otp()

    if send_otp_twilio(user.country_code,user.phone_number, otp_code):
        store_otp(db,user.phone_number, otp_code)  # ✅ Store OTP in DB
    else:
        raise HTTPException(status_code=500, detail="Failed to send OTP. Try again.")

    new_user = User(
        full_name=user.full_name,
        email=user.email,
        phone_number=user.phone_number,
        password_hash=hash_password(user.password),
        isVerified=False
    )
    db.add(new_user)
    db.commit()

    return {"message": "OTP sent to your phone. Please verify to complete signup."}


# ✅ Detects whether the identifier is an email or phone number
def is_email(identifier: str) -> bool:
    return "@" in identifier

# ✅ Combined Login Route for Email & Phone Login
@auth_router.post("/login")
async def login(user: UserEmailLogin, db: Session = Depends(get_db)):
    """Handles login using email/password."""
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    if not db_user.isVerified:
        raise HTTPException(status_code=403, detail="Account not verified. Please verify OTP.")

    # ✅ Generate JWT token after successful login
    token = create_access_token(db_user.email)
    return {"message": "Login successful", "access_token": token, "token_type": "bearer"}

@auth_router.post("/verify-otp", status_code=status.HTTP_200_OK)
def verify_otp(data: OTPVerification, db: Session = Depends(get_db)):
    """Verifies OTP and activates user account."""
    otp_record = db.query(OTP).filter(
        (OTP.phone_number == data.phone_number) & (OTP.otp_code == data.otp)
    ).first()

    if not otp_record:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    # ✅ Convert expires_at to timezone-aware datetime
    expires_at_aware = otp_record.expires_at.replace(tzinfo=timezone.utc)

    if expires_at_aware < datetime.now(timezone.utc):
        db.delete(otp_record)  # ✅ Automatically delete expired OTPs
        db.commit()
        raise HTTPException(status_code=400, detail="OTP has expired. Please request a new one.")

    user = db.query(User).filter(User.phone_number == data.phone_number).first()

    if user:
        user.isVerified = True
        db.commit()
        db.refresh(user)

    db.delete(otp_record)  # ✅ Delete OTP after successful verification
    db.commit()

    return {"message": "Phone number verified successfully. You can now log in."}