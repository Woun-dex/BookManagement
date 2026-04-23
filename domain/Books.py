import pydantic
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from config.dbConfig import Base


class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    author = Column(String, index=True)
    category = Column(String, index=True)
    image = Column(String, index=True)
    stock = Column(Integer, index=True)
    year = Column(Integer, index=True)
    language = Column(String, index=True)
    pages = Column(Integer, index=True)
    isbn = Column(String, index=True)
    

class BookCreate(pydantic.BaseModel):
    title: str
    description: str
    author: str
    category: str
    image: str
    stock: int
    year: int
    language: str
    pages: int
    isbn: str

class BookUpdate(pydantic.BaseModel):
    title: str
    description: str
    author: str
    category: str
    image: str
    stock: int
    year: int
    language: str
    pages: int
    isbn: str

class BookDelete(pydantic.BaseModel):
    id: int