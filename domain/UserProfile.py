import pydantic
from sqlalchemy import Column, Integer, String
from config.dbConfig import Base

class UserProfile(Base):
    __tablename__ = "user_profiles"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    profile_picture = Column(String, index=True)
    bio = Column(String, index=True)
    phone_number = Column(String, index=True)    

class UserProfileCreate(pydantic.BaseModel):
    user_id: int
    profile_picture: str | None = None
    bio: str | None = None
    phone_number: str | None = None

class UserProfileUpdate(pydantic.BaseModel):
    id: int
    user_id: int
    profile_picture: str | None = None
    bio: str | None = None
    phone_number: str | None = None

class UserProfileDelete(pydantic.BaseModel):
    id: int