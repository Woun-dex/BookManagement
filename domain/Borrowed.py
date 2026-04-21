import pydantic
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from config.dbConfig import Base

class Borrowed(Base):
    __tablename__ = "borrowed"
    id = Column(Integer, primary_key=True, index=True)
    reader_id = Column(Integer, index=True)
    librarian_id = Column(Integer, index=True)
    book_id = Column(Integer, index=True)
    borrow_date = Column(String, index=True)
    return_date = Column(String, index=True)
    state = Column(String, index=True)

class BorrowedCreate(pydantic.BaseModel):
    reader_id: int
    librarian_id: int
    book_id: int
    borrow_date: str
    return_date: str
    state: str

class BorrowedUpdate(pydantic.BaseModel):
    reader_id: int
    librarian_id: int
    book_id: int
    borrow_date: str
    return_date: str
    state: str

class BorrowedDelete(pydantic.BaseModel):
    id: int