import domain.user as User
import domain.UserProfile as UserProfile
import service.auth.authHelper as AuthHelper
from fastapi.security import OAuth2PasswordBearer , OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, Request
from config.dbConfig import get_db_session
from fastapi.responses import JSONResponse


def register(user: User.UserCreate) -> User.User:
    hashed_password = AuthHelper.hash_password(user.password)
    with get_db_session() as db:
        new_user = User.User(full_name=user.full_name, email=user.email, role=user.role, password=hashed_password)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        # Create an empty profile for the new user
        new_profile = UserProfile.UserProfile(user_id=new_user.id)
        db.add(new_profile)
        db.commit()
        
        return new_user

def login(user: User.UserLogin):
    with get_db_session() as db:
        found_user = db.query(User.User).filter(User.User.email == user.email).first()
        if not found_user:
            raise HTTPException(status_code=404, detail="User not found")
        if not AuthHelper.verify_password(user.password, found_user.password):
            raise HTTPException(status_code=401, detail="Invalid password")
            
        token_data = AuthHelper.tokenData(
            id=found_user.id,
            full_name=found_user.full_name,
            email=found_user.email,
            role=found_user.role
        )
        token = AuthHelper.create_token(token_data)
        token_str = token.access_token
        response = JSONResponse(content={"message": "Login successful", "token": token_str})
        response.set_cookie(key="token", value=token_str, httponly=False, samesite="lax")
        return response

def loginLibrarian(user: User.UserLogin):
    with get_db_session() as db:
        found_user = db.query(User.User).filter(User.User.email == user.email).first()
        if not found_user:
            raise HTTPException(status_code=404, detail="User not found")
        
        if not AuthHelper.verify_password(user.password, found_user.password):
            raise HTTPException(status_code=401, detail="Invalid password")
        
        if found_user.role != "librarian":
            raise HTTPException(status_code=403, detail="User is not a librarian")
            
        token_data = AuthHelper.tokenData(
            id=found_user.id,
            full_name=found_user.full_name,
            email=found_user.email,
            role=found_user.role
        )
        token = AuthHelper.create_token(token_data)
        token_str = token.access_token
        response = JSONResponse(content={"message": "Login successful", "token": token_str})
        response.set_cookie(key="token", value=token_str, httponly=False, samesite="lax")
        return response


def get_current_user(request: Request):
    user = request.state.user
    return user

def update_user(user_id: int, user_update: User.UserUpdate):
    with get_db_session() as db:
        existing_user = db.query(User.User).filter(User.User.id == user_id).first()
        if not existing_user:
            raise HTTPException(status_code=404, detail="User not found")
        
        existing_user.full_name = user_update.full_name
        existing_user.email = user_update.email
        # Update password only if provided
        if user_update.password:
            existing_user.password = AuthHelper.hash_password(user_update.password)
            
        db.commit()
        db.refresh(existing_user)
        return existing_user