from fastapi import APIRouter , Depends , HTTPException , Request
import domain.Books as Books
import domain.Borrowed as Borrowed
from config.dbConfig import get_db
from datetime import datetime, timedelta
import service.LibrarianService as LibrarianService


router = APIRouter()

@router.get("/borrowed")
def get_all_borrowed(request: Request , page : int = 1 , limit : int = 10 , sort_by : str = "id" , sort_order : str = "asc"):
    if request.state.user.role != "librarian":
        raise HTTPException(status_code=403, detail="User is not a librarian")
    return LibrarianService.get_all_borrowed(page , limit , sort_by , sort_order)

@router.get("/borrowed/{id}")
def get_borrowed(request: Request , id : int):
    if request.state.user.role != "librarian":
        raise HTTPException(status_code=403, detail="User is not a librarian")
    return LibrarianService.get_borrowed(id)

@router.get("/borrowed/reader/{reader_id}")
def get_borrowed_by_reader(request: Request , reader_id : int , page : int = 1 , limit : int = 10 , sort_by : str = "id" , sort_order : str = "asc"):
    if request.state.user.role != "librarian":
        raise HTTPException(status_code=403, detail="User is not a librarian")
    return LibrarianService.get_borrowed_by_reader(reader_id , page , limit , sort_by , sort_order)

@router.get("/borrowed/librarian/{librarian_id}")
def get_borrowed_by_librarian(request: Request , librarian_id : int , page : int = 1 , limit : int = 10 , sort_by : str = "id" , sort_order : str = "asc"):
    if request.state.user.role != "librarian":
        raise HTTPException(status_code=403, detail="User is not a librarian")
    return LibrarianService.get_borrowed_by_librarian(librarian_id , page , limit , sort_by , sort_order)

@router.get("/borrowed/book/{book_id}")
def get_borrowed_by_book(request: Request , book_id : int , page : int = 1 , limit : int = 10 , sort_by : str = "id" , sort_order : str = "asc"):
    if request.state.user.role != "librarian":
        raise HTTPException(status_code=403, detail="User is not a librarian")
    return LibrarianService.get_borrowed_by_book(book_id , page , limit , sort_by , sort_order)

@router.get("/borrowed/borrow_date/{borrow_date}")
def get_borrowed_by_borrow_date(request: Request , borrow_date : str , page : int = 1 , limit : int = 10 , sort_by : str = "id" , sort_order : str = "asc"):
    if request.state.user.role != "librarian":
        raise HTTPException(status_code=403, detail="User is not a librarian")
    return LibrarianService.get_borrowed_by_borrow_date(borrow_date , page , limit , sort_by , sort_order)

@router.get("/borrowed/return_date/{return_date}")
def get_borrowed_by_return_date(request: Request , return_date : str , page : int = 1 , limit : int = 10 , sort_by : str = "id" , sort_order : str = "asc"):
    if request.state.user.role != "librarian":
        raise HTTPException(status_code=403, detail="User is not a librarian")
    return LibrarianService.get_borrowed_by_return_date(return_date , page , limit , sort_by , sort_order)

@router.post("/borrowed")
def add_borrowed(request:Request):
    db = get_db()
    Book = db.query(Books.Book).filter(Books.Book.id == request.state.bookId).first()
    if not Book:
        raise HTTPException(status_code=404, detail="Book not found")
    if Book.stock == 0:
        raise HTTPException(status_code=400, detail="Book is out of stock")
    Book.stock -= 1
    borrowed = Borrowed.Borrowed(
        book_id = request.state.bookId,
        reader_id = request.state.readerId,
        librarian_id = request.state.user.id,
        borrow_date = datetime.now(),
        return_date = datetime.now() + timedelta(days=14),
        state = "borrowed"
    )
    db.merge(Book)
    db.commit()
    db.refresh(Book)
    return Book

@router.put("/borrowed")
def update_borrowed(request: Request , borrowed: Borrowed.BorrowedUpdate):
    if request.state.user.role != "librarian":
        raise HTTPException(status_code=403, detail="User is not a librarian")
    return LibrarianService.update_borrowed(borrowed)

@router.put("/return_borrowed/{bookId}")
def return_borrowed(request: Request , bookId : int):
    db = get_db()
    Book = db.query(Books.Book).filter(Books.Book.id == bookId).first()
    if not Book:
        raise HTTPException(status_code=404, detail="Book not found")
    Book.stock += 1
    borrowed = db.query(Borrowed.Borrowed).filter(Borrowed.Borrowed.book_id == bookId).first()
    if not borrowed:
        raise HTTPException(status_code=404, detail="Borrowed not found")
    borrowed.return_date = datetime.now()
    borrowed.state = "returned"
    db.merge(borrowed)
    db.merge(Book)
    db.commit()
    db.refresh(Book)
    db.refresh(borrowed)
    return Book
