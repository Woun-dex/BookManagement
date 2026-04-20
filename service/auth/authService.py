import domain.user as User
import service.auth.authHelper as AuthHelper
from fastapi.security import OAuth2PasswordBearer , OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException
from config.dbConfig import get_db

def register(user: User.UserCreate) -> User.User:
    hashed_password = AuthHelper.hash_password(user.password)
    user.password = hashed_password
    db = get_db()
    db.add(user)
    db.commit()
    db.refresh(user)
    return User.User(**user.dict())

def login(user: User.UserLogin) -> User.User:
    db = get_db()
    user = db.query(User.User).filter(User.User.email == user.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not AuthHelper.verify_password(user.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid password")
    return User.User(**user.dict())

def loginLibrarian(user: User.UserLogin) -> User.User:
    db = get_db()
    user = db.query(User.User).filter(User.User.email == user.email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not AuthHelper.verify_password(user.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid password")
    if user.role != "librarian":
        raise HTTPException(status_code=403, detail="User is not a librarian")
    return User.User(**user.dict())


def get_current_user(token: str = Depends(OAuth2PasswordBearer(tokenUrl="token"))):
    return AuthHelper.decode_token(token)
