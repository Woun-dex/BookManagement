import domain.Books as Book
import domain.BooksRate as BooksRate
from config.dbConfig import get_db_session
import service.LLMService as LLMService

def get_all_books(page: int, limit: int , sort_by: str , sort_order: str):
    with get_db_session() as db:
        col = getattr(Book.Book, sort_by)
        order_expr = col.desc() if sort_order.lower() == "desc" else col.asc()
        return db.query(Book.Book).order_by(order_expr).offset((page - 1) * limit).limit(limit).all() 

def get_book(id: int):
    with get_db_session() as db:
        return db.query(Book.Book).filter(Book.Book.id == id).first()

def get_books_by_title(title: str , page : int , limit : int, sort_by: str, sort_order: str):
    with get_db_session() as db:
        col = getattr(Book.Book, sort_by)
        order_expr = col.desc() if sort_order.lower() == "desc" else col.asc()
        return db.query(Book.Book).filter(Book.Book.title == title).order_by(order_expr).offset((page - 1) * limit).limit(limit).all()

def get_books_by_author(author: str , page : int , limit : int, sort_by: str, sort_order: str):
    with get_db_session() as db:
        col = getattr(Book.Book, sort_by)
        order_expr = col.desc() if sort_order.lower() == "desc" else col.asc()
        return db.query(Book.Book).filter(Book.Book.author == author).order_by(order_expr).offset((page - 1) * limit).limit(limit).all()

def get_books_by_category(category: str , page : int , limit : int, sort_by: str, sort_order: str):
    with get_db_session() as db:
        col = getattr(Book.Book, sort_by)
        order_expr = col.desc() if sort_order.lower() == "desc" else col.asc()
        return db.query(Book.Book).filter(Book.Book.category == category).order_by(order_expr).offset((page - 1) * limit).limit(limit).all()

def get_books_by_rate(rate: int, page : int , limit : int , sort_by: str, sort_order : str):
    with get_db_session() as db:
        # Assuming sort_by is applicable to Book.Book.
        # We filter by the provided rate value, but the current model might need adjusting.
        col = getattr(Book.Book, sort_by)
        order_expr = col.desc() if sort_order.lower() == "desc" else col.asc()
        return db.query(Book.Book).join(BooksRate.BooksRate).filter(BooksRate.BooksRate.rate == rate).order_by(order_expr).offset((page - 1) * limit).limit(limit).all()

def search_books(query: str, page: int = 1, limit: int = 10, sort_by: str = "id", sort_order: str = "asc"):
    with get_db_session() as db:
        col = getattr(Book.Book, sort_by)
        order_expr = col.desc() if sort_order.lower() == "desc" else col.asc()
        return db.query(Book.Book).filter(
            Book.Book.title.ilike(f"%{query}%") | Book.Book.author.ilike(f"%{query}%")
        ).order_by(order_expr).offset((page - 1) * limit).limit(limit).all()



def create_book(book: Book.BookCreate):
    with get_db_session() as db:
        new_book = Book.Book(**book.dict())
        db.add(new_book)
        db.commit()
        db.refresh(new_book)
        return new_book

def update_book(book: Book.BookUpdate):
    with get_db_session() as db:
        updated_book = Book.Book(**book.dict())
        db.merge(updated_book)
        db.commit()
        return updated_book

def delete_book(book: Book.BookDelete):
    with get_db_session() as db:
        book_to_delete = db.query(Book.Book).filter(Book.Book.id == book.id).first()
        if book_to_delete:
            db.delete(book_to_delete)
            db.commit()
        return book_to_delete

def generate_book_brief(title: str, author: str, category: str):
    return LLMService.generate_book_brief(title, author, category)