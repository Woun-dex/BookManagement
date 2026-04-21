import domain.user as User
import service.auth.authHelper as AuthHelper
from fastapi.security import OAuth2PasswordBearer , OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, Request
from config.dbConfig import get_db

def register(user: User.UserCreate) -> User.User:
    hashed_password = AuthHelper.hash_password(user.password)
    db = next(get_db())
    new_user = User.User(full_name=user.full_name, email=user.email, role=user.role, password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

def login(user: User.UserLogin):
    db = next(get_db())
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
    return token

def loginLibrarian(user: User.UserLogin):
    db = next(get_db())
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
    return token


def get_current_user(request: Request):
    user = request.state.user
    return user