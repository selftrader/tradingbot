from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.connection import get_db
from database.models import User
from services.auth_service import get_current_user  # ✅ Middleware for authentication

router = APIRouter()

@router.get("/profile")
def get_user_profile(current_user: User = Depends(get_current_user)):
    """Fetch the currently logged-in user's profile"""
    return {"email": current_user.email, "name": current_user.full_name}

@router.put("/profile")
def update_user_profile(name: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Update the user's profile name"""
    current_user.name = name
    db.commit()
    return {"message": "Profile updated successfully"}
