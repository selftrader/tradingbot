import os
import random
from requests import Session
from twilio.rest import Client
from datetime import datetime, timedelta, timezone
from database.connection import SessionLocal
from database.models import OTP
from dotenv import load_dotenv

load_dotenv()

# Twilio Credentials from .env
TWILIO_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE = os.getenv("TWILIO_PHONE_NUMBER")

# ✅ Generate a 6-digit OTP
def generate_otp():
    return str(random.randint(100000, 999999))

# ✅ Send OTP via Twilio SMS
def send_otp_twilio(country_code,phone_number: str, otp: str):
    """Sends OTP using Twilio SMS API."""
    full_phone_number = f"{country_code}{phone_number}"
    try:
        client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=f"Your OTP for signup is: {otp}",
            from_=TWILIO_PHONE,
            to=full_phone_number
        )
        print(f"OTP sent to {phone_number}")
        return True
    except Exception as e:
        print(f"Error sending OTP: {e}")
        return False

# ✅ Save OTP in Database
def store_otp(db: Session, phone_number: str, otp_code: str):
    existing_otp = db.query(OTP).filter(OTP.phone_number == phone_number).first()

    if existing_otp:
        # ✅ Update existing OTP instead of inserting a duplicate
        existing_otp.otp_code = otp_code
        existing_otp.expires_at = datetime.now(timezone.utc) + timedelta(minutes=5)
    else:
        # ✅ Insert new OTP if no existing record
        new_otp = OTP(
            phone_number=phone_number,
            otp_code=otp_code,
            expires_at=datetime.now(timezone.utc) + timedelta(minutes=5)
        )
        db.add(new_otp)

    db.commit()
