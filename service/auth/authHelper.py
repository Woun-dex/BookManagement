from pwdlib import PasswordHash
import jwt
import pydantic
from datetime import datetime, timedelta

class token(pydantic.BaseModel):
    access_token: str
    token_type: str

class tokenData(pydantic.BaseModel):
    id: int
    full_name: str
    email: str
    role: str

SECRET_KEY = "secret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

password_hash = PasswordHash.recommended()

def hash_password(password: str) -> str:
    return password_hash.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)

def create_token(TokenData: tokenData) -> token:
    to_encode = TokenData.dict()
    to_encode.update({"exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token(access_token=encoded_jwt, token_type="bearer")

def decode_token(token: str) -> tokenData:
    return tokenData(**jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]))


