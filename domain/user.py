import pydantic
from sqlalchemy import Column, Integer, String
from config.dbConfig import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, index=True)
    password = Column(String, index=True)
    role = Column(String, index=True)

class UserCreate(pydantic.BaseModel):
    full_name: str
    email: str
    password: str
    role: str

class UserUpdate(pydantic.BaseModel):
    full_name: str
    email: str
    password: str
    role: str

class UserDelete(pydantic.BaseModel):
    id: int

class UserLogin(pydantic.BaseModel):
    email: str
    password: str
