from datetime import datetime, timedelta, timezone
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
import jwt
from sqlalchemy.orm import Session
from core.config import REFRESH_SECRET
from database.schemas import UserEmailLogin, UserSignup, OTPVerification
from database.connection import get_db
from database.models import OTP, User
from passlib.context import CryptContext
from services.otp_service import generate_otp, send_otp_twilio, store_otp
from services.auth_service import (
    SECRET_KEY,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_DAYS,
    ALGORITHM,
    verify_password,
    create_access_token,
    create_refresh_token,
)

# ✅ Password Hashing Context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

auth_router = APIRouter()


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

    # ✅ Generate and Send OTP
    otp_code = generate_otp()
    if not send_otp_twilio(user.country_code, user.phone_number, otp_code):
        raise HTTPException(status_code=500, detail="Failed to send OTP. Try again.")

    store_otp(db, user.phone_number, otp_code)

    # ✅ Create User with **hashed password**
    new_user = User(
        full_name=user.full_name,
        email=user.email,
        phone_number=user.phone_number,
        password_hash=pwd_context.hash(user.password),  # ✅ Hash password
        isVerified=False
    )
    db.add(new_user)
    db.commit()

    return {"message": "OTP sent to your phone. Please verify to complete signup."}


# ✅ OTP Verification Route
@auth_router.post("/verify-otp", status_code=status.HTTP_200_OK)
def verify_otp(data: OTPVerification, db: Session = Depends(get_db)):
    """Verifies OTP and activates user account."""
    otp_record = db.query(OTP).filter(
        (OTP.phone_number == data.phone_number) & (OTP.otp_code == data.otp)
    ).first()

    if not otp_record:
        raise HTTPException(status_code=400, detail="Invalid OTP")

    # ✅ Ensure OTP is not expired
    if otp_record.expires_at.replace(tzinfo=timezone.utc) < datetime.now(timezone.utc):
        db.delete(otp_record)
        db.commit()
        raise HTTPException(status_code=400, detail="OTP has expired. Please request a new one.")

    # ✅ Mark user as verified
    user = db.query(User).filter(User.phone_number == data.phone_number).first()
    if user:
        user.isVerified = True
        db.commit()
        db.refresh(user)

    # ✅ Delete OTP after verification
    db.delete(otp_record)
    db.commit()

    return {"message": "Phone number verified successfully. You can now log in."}


# ✅ Login Route with JWT Token Generation
@auth_router.post("/login")
def login(user: UserEmailLogin, response: Response, db: Session = Depends(get_db)):
    """Handles user login and sets refresh token in cookies."""
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user or not verify_password(user.password, db_user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not db_user.isVerified:
        raise HTTPException(status_code=403, detail="Account not verified. Please verify OTP.")

    # ✅ Generate JWT tokens
    access_token = create_access_token(db_user.email)
    refresh_token = create_refresh_token(db_user.email)  # ✅ FIXED: Uses `create_refresh_token()`

    # ✅ Store `refresh_token` in HTTP-Only Cookie
    response.set_cookie(key="access_token", value=access_token, httponly=True, secure=True, samesite="Lax")
    response.set_cookie(key="refresh_token", value=refresh_token, httponly=True, secure=True, samesite="Lax")

    return {"message": "Login successful", "access_token": access_token, "token_type": "bearer","refresh_token": refresh_token, "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES}


# ✅ Refresh Token Route (for auto-login)
@auth_router.post("/refresh-token")
def refresh_token(request: Request, db: Session = Depends(get_db)):
    """Refresh access token using a valid refresh token"""
    refresh_token = request.headers.get("Refresh-Token")

    if not refresh_token:
        raise HTTPException(status_code=401, detail="Refresh token missing")

    try:
        payload = jwt.decode(refresh_token, REFRESH_SECRET, algorithms=[ALGORITHM])
        user_email = payload.get("sub")
        if not user_email:
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        
        user = db.query(User).filter(User.email == user_email).first()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        # ✅ Generate a new access token
        access_token = create_access_token({"sub": user.email})
        
        return {"access_token": access_token}
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")




# ✅ Logout API - Clears Refresh Token
@auth_router.post("/logout")
def logout(response: Response):
    """Clears refresh token from cookies (Logs user out)."""
    response.delete_cookie("refresh_token")
    return {"message": "Logged out successfully"}
