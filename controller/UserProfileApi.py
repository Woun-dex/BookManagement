from fastapi import APIRouter, Request, Depends
import service.UserProfileService as UserProfileService
import domain.UserProfile as UserProfile

router = APIRouter()

@router.get("/profile/user/{user_id}")
def get_profile_by_user_id(user_id: int):
    return UserProfileService.get_profile_by_user_id(user_id)

@router.get("/profile/{id}")
def get_profile_by_id(id: int):
    return UserProfileService.get_profile_by_id(id)

@router.put("/profile")
def update_profile(profile: UserProfile.UserProfileUpdate):
    return UserProfileService.update_profile(profile)

@router.delete("/user-profile")
def delete_profile(profile: UserProfile.UserProfileDelete):
    return UserProfileService.delete_profile(profile)

import service.auth.authService as AuthService

@router.get("/profile/me")
def get_my_profile(user = Depends(AuthService.get_current_user)):
    return UserProfileService.get_profile_by_user_id(user["id"])
