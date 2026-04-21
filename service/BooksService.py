import domain.Books as Book
import domain.BooksRate as BooksRate
from config.dbConfig import get_db
import service.LLMService as LLMService

def get_all_books(page: int, limit: int , sort_by: str , sort_order: str):
    db = next(get_db())
    return db.query(Book.Book).offset((page - 1) * limit).limit(limit).order_by(getattr(Book.Book, sort_by), sort_order).all() 

def get_book(id: int):
    db = next(get_db())
    return db.query(Book.Book).filter(Book.Book.id == id)

def get_books_by_title(title: str , page : int , limit : int):
    db = next(get_db())
    return db.query(Book.Book).filter(Book.Book.title == title).offset((page - 1) * limit).limit(limit).all()

def get_books_by_author(author: str , page : int , limit : int):
    db = next(get_db())
    return db.query(Book.Book).filter(Book.Book.author == author).offset((page - 1) * limit).limit(limit).all()

def get_books_by_category(category: str , page : int , limit : int):
    db = next(get_db())
    return db.query(Book.Book).filter(Book.Book.category == category).offset((page - 1) * limit).limit(limit).all()

def get_books_by_rate(page : int , limit : int , sort_order : str):
    db = next(get_db())
    return db.query(Book.Book).join(BooksRate.BooksRate).offset((page - 1) * limit).limit(limit).order_by(getattr(BooksRate.BooksRate, "rate"), sort_order).all()



def create_book(book: Book.BookCreate):
    db = next(get_db())
    new_book = Book.Book(**book.dict())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book

def update_book(book: Book.BookUpdate):
    db = next(get_db())
    updated_book = Book.Book(**book.dict())
    db.merge(updated_book)
    db.commit()
    return updated_book

def delete_book(book: Book.BookDelete):
    db = next(get_db())
    book_to_delete = db.query(Book.Book).filter(Book.Book.id == book.id).first()
    if book_to_delete:
        db.delete(book_to_delete)
        db.commit()
    return book_to_delete

def generate_book_brief(title: str, author: str, category: str):
    return LLMService.generate_book_brief(title, author, category)