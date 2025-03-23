from fastapi import HTTPException
from sqlalchemy.orm import Session
from database.models import User
from database.schemas import UserResponse, UserProfileUpdate

def get_user_profile(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"name": user.full_name, "email": user.email,
            "phone": user.phone_number,
            "brokerAccounts": user.broker_configs
            }

def update_user_profile(db: Session, user_id: int, data: UserProfileUpdate):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.name = data.name
    db.commit()
    return {"message": "Profile updated successfully"}
