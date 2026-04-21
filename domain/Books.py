import pydantic
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from config.dbConfig import Base


class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author = Column(String, index=True)
    category = Column(String, index=True)
    cover_image = Column(String, index=True)
    stock = Column(Integer, index=True)

class BookCreate(pydantic.BaseModel):
    title: str
    author: str
    category: str
    cover_image: str
    stock: int

class BookUpdate(pydantic.BaseModel):
    title: str
    author: str
    category: str
    cover_image: str
    stock: int

class BookDelete(pydantic.BaseModel):
    id: int