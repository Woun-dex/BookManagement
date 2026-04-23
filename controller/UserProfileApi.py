from fastapi import APIRouter, Request, Depends
import service.UserProfileService as UserProfileService
import domain.UserProfile as UserProfile

router = APIRouter()

@router.get("/user-profile/user/{user_id}")
def get_profile_by_user_id(user_id: int):
    return UserProfileService.get_profile_by_user_id(user_id)

@router.get("/user-profile/{id}")
def get_profile_by_id(id: int):
    return UserProfileService.get_profile_by_id(id)

@router.put("/user-profile")
def update_profile(profile: UserProfile.UserProfileUpdate):
    return UserProfileService.update_profile(profile)

@router.delete("/user-profile")
def delete_profile(profile: UserProfile.UserProfileDelete):
    return UserProfileService.delete_profile(profile)
