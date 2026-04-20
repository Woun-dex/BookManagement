import domain.Books as Book
import domain.BooksRate as BooksRate
from config.dbConfig import get_db

def get_all_books(page: int, limit: int , sort_by: str , sort_order: str):
    db = get_db()
    return db.query(Book.Book).offset((page - 1) * limit).limit(limit).order_by(getattr(Book.Book, sort_by), sort_order).all() 

def get_book(id: int):
    db = get_db()
    return db.query(Book.Book).filter(Book.Book.id == id)

def get_books_by_title(title: str , page : int , limit : int):
    db = get_db()
    return db.query(Book.Book).filter(Book.Book.title == title).offset((page - 1) * limit).limit(limit).all()

def get_books_by_author(author: str , page : int , limit : int):
    db = get_db()
    return db.query(Book.Book).filter(Book.Book.author == author).offset((page - 1) * limit).limit(limit).all()

def get_books_by_category(category: str , page : int , limit : int):
    db = get_db()
    return db.query(Book.Book).filter(Book.Book.category == category).offset((page - 1) * limit).limit(limit).all()

def get_books_by_rate(page : int , limit : int , sort_order : str):
    db = get_db()
    return db.query(Book.Book).join(BooksRate.BooksRate).offset((page - 1) * limit).limit(limit).order_by(getattr(BooksRate.BooksRate, "rate"), sort_order).all()



def create_book(book: Book.BookCreate):
    db = get_db()
    db.add(book)
    db.commit()
    db.refresh(book)
    return Book.Book(**book.dict())

def update_book(book: Book.BookUpdate):
    db = get_db()
    db.merge(book)
    db.commit()
    db.refresh(book)
    return Book.Book(**book.dict())

def delete_book(book: Book.BookDelete):
    db = get_db()
    db.delete(book)
    db.commit()
    return Book.Book(**book.dict())