import domain.UserProfile as UserProfile
from config.dbConfig import get_db
from fastapi import HTTPException

def get_profile_by_user_id(user_id: int):
    db = next(get_db())
    profile = db.query(UserProfile.UserProfile).filter(UserProfile.UserProfile.user_id == user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

def get_profile_by_id(profile_id: int):
    db = next(get_db())
    profile = db.query(UserProfile.UserProfile).filter(UserProfile.UserProfile.id == profile_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

def update_profile(profile_update: UserProfile.UserProfileUpdate):
    db = next(get_db())
    existing_profile = db.query(UserProfile.UserProfile).filter(UserProfile.UserProfile.id == profile_update.id).first()
    if not existing_profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    
    update_data = profile_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(existing_profile, key, value)
    
    db.commit()
    db.refresh(existing_profile)
    return existing_profile

def delete_profile(profile_delete: UserProfile.UserProfileDelete):
    db = next(get_db())
    profile_to_delete = db.query(UserProfile.UserProfile).filter(UserProfile.UserProfile.id == profile_delete.id).first()
    if profile_to_delete:
        db.delete(profile_to_delete)
        db.commit()
    return profile_to_delete
