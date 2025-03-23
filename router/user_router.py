from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.connection import get_db
from database.models import User
from database.schemas import UserProfileUpdate
from services.auth_service import get_current_user
from services.user_service import get_user_profile, update_user_profile  # ✅ Middleware for authentication

router = APIRouter()

@router.get("/profile")
def profile(db: Session = Depends(get_db), user_id: int = 1):  # Replace with actual user ID from auth
    return get_user_profile(db, user_id)

@router.put("/profile/update")
def update_profile(data: UserProfileUpdate, db: Session = Depends(get_db), user_id: int = 1):
    return update_user_profile(db, user_id, data)