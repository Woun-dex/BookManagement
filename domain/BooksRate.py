import pydantic
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from config.dbConfig import Base

class BooksRate(Base):
    __tablename__ = "books_rate"
    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer, index=True)
    user_id = Column(Integer, index=True)
    rate = Column(Integer, index=True)
    review = Column(String, index=True)

class BooksRateCreate(pydantic.BaseModel):
    book_id: int
    user_id: int
    rate: int
    review: str

class BooksRateUpdate(pydantic.BaseModel):
    book_id: int
    user_id: int
    rate: int
    review: str

class BooksRateDelete(pydantic.BaseModel):
    id: int