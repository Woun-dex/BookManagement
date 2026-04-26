import pydantic
from fastapi import APIRouter , Depends , HTTPException , Request , Response
import domain.Books as Books
import domain.Borrowed as Borrowed
from config.dbConfig import get_db_session
from datetime import datetime, timedelta
import service.LibrarianService as LibrarianService


router = APIRouter()

@router.get("/borrowed")
def get_all_borrowed(request: Request , page : int = 1 , limit : int = 10 , sort_by : str = "id" , sort_order : str = "asc"):
    if request.state.user.get("role") != "librarian":
        raise HTTPException(status_code=403, detail="User is not a librarian")
    return LibrarianService.get_all_borrowed(page , limit , sort_by , sort_order)

@router.get("/borrowed/{id}")
def get_borrowed(request: Request , id : int):
    if request.state.user.get("role") != "librarian":
        raise HTTPException(status_code=403, detail="User is not a librarian")
    return LibrarianService.get_borrowed(id)

@router.get("/borrowed/reader/{reader_id}")
def get_borrowed_by_reader(request: Request , reader_id : int , page : int = 1 , limit : int = 10 , sort_by : str = "id" , sort_order : str = "asc"):
    # Readers can only view their own borrowed books; librarians can view any
    user_role = request.state.user.get("role")
    user_id = request.state.user.get("id")
    if user_role != "librarian" and user_id != reader_id:
        raise HTTPException(status_code=403, detail="Access denied")
    return LibrarianService.get_borrowed_by_reader(reader_id , page , limit , sort_by , sort_order)

@router.get("/borrowed/librarian/{librarian_id}")
def get_borrowed_by_librarian(request: Request , librarian_id : int , page : int = 1 , limit : int = 10 , sort_by : str = "id" , sort_order : str = "asc"):
    if request.state.user.get("role") != "librarian":
        raise HTTPException(status_code=403, detail="User is not a librarian")
    return LibrarianService.get_borrowed_by_librarian(librarian_id , page , limit , sort_by , sort_order)

@router.get("/borrowed/book/{book_id}")
def get_borrowed_by_book(request: Request , book_id : int , page : int = 1 , limit : int = 10 , sort_by : str = "id" , sort_order : str = "asc"):
    if request.state.user.get("role") != "librarian":
        raise HTTPException(status_code=403, detail="User is not a librarian")
    return LibrarianService.get_borrowed_by_book(book_id , page , limit , sort_by , sort_order)

@router.get("/borrowed/borrow_date/{borrow_date}")
def get_borrowed_by_borrow_date(request: Request , borrow_date : str , page : int = 1 , limit : int = 10 , sort_by : str = "id" , sort_order : str = "asc"):
    if request.state.user.get("role") != "librarian":
        raise HTTPException(status_code=403, detail="User is not a librarian")
    return LibrarianService.get_borrowed_by_borrow_date(borrow_date , page , limit , sort_by , sort_order)

@router.get("/borrowed/return_date/{return_date}")
def get_borrowed_by_return_date(request: Request , return_date : str , page : int = 1 , limit : int = 10 , sort_by : str = "id" , sort_order : str = "asc"):
    if request.state.user.get("role") != "librarian":
        raise HTTPException(status_code=403, detail="User is not a librarian")
    return LibrarianService.get_borrowed_by_return_date(return_date , page , limit , sort_by , sort_order)

class AddBorrowedRequest(pydantic.BaseModel):
    bookId: int
    readerId: int
    returnDate: str

@router.post("/borrowed")
def add_borrowed(request: Request, payload: AddBorrowedRequest):
    with get_db_session() as db:
        book = db.query(Books.Book).filter(Books.Book.id == payload.bookId).first()
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        
        borrowed = Borrowed.Borrowed(
            book_id = payload.bookId,
            reader_id = payload.readerId,
            librarian_id = request.state.user.get("id"),
            borrow_date = datetime.now().strftime("%Y-%m-%d"),
            return_date = datetime.strptime(payload.returnDate, "%Y-%m-%d"),
            state = "pending"
        )
        db.add(borrowed)
        db.commit()
        db.refresh(borrowed)
        return borrowed

@router.put("/approve_borrowed/{id}")
def approve_borrowed(request: Request, id: int):
    if request.state.user.get("role") != "librarian":
        raise HTTPException(status_code=403, detail="User is not a librarian")
    with get_db_session() as db:
        borrowed = db.query(Borrowed.Borrowed).filter(Borrowed.Borrowed.id == id).first()
        if not borrowed:
            raise HTTPException(status_code=404, detail="Request not found")
        
        book = db.query(Books.Book).filter(Books.Book.id == borrowed.book_id).first()
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        
        if book.stock <= 0:
            raise HTTPException(status_code=400, detail="Book is out of stock")
        
        book.stock -= 1
        borrowed.state = "borrowed"
        borrowed.borrow_date = datetime.now().strftime("%Y-%m-%d")
        # Only set return_date if it wasn't already specified in the original request
        if not borrowed.return_date:
            borrowed.return_date = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")
        
        db.merge(book)
        db.merge(borrowed)
        db.commit()
        return borrowed

@router.put("/reject_borrowed/{id}")
def reject_borrowed(request: Request, id: int):
    if request.state.user.get("role") != "librarian":
        raise HTTPException(status_code=403, detail="User is not a librarian")
    with get_db_session() as db:
        borrowed = db.query(Borrowed.Borrowed).filter(Borrowed.Borrowed.id == id).first()
        if not borrowed:
            raise HTTPException(status_code=404, detail="Request not found")
        
        borrowed.state = "rejected"
        db.merge(borrowed)
        db.commit()
        return borrowed

@router.put("/borrowed")
def update_borrowed(request: Request , borrowed: Borrowed.BorrowedUpdate):
    if request.state.user.get("role") != "librarian":
        raise HTTPException(status_code=403, detail="User is not a librarian")
    return LibrarianService.update_borrowed(borrowed)

@router.put("/return_borrowed/{bookId}")
def return_borrowed(request: Request , bookId : int):
    if request.state.user.get("role") != "librarian":
        raise HTTPException(status_code=403, detail="User is not a librarian")
    with get_db_session() as db:
        book = db.query(Books.Book).filter(Books.Book.id == bookId).first()
        if not book:
            raise HTTPException(status_code=404, detail="Book not found")
        book.stock += 1
        borrowed = db.query(Borrowed.Borrowed).filter(Borrowed.Borrowed.book_id == bookId).first()
        if not borrowed:
            raise HTTPException(status_code=404, detail="Borrowed not found")
        borrowed.return_date = datetime.now()
        borrowed.state = "returned"
        db.merge(borrowed)
        db.merge(book)
        db.commit()
        db.refresh(book)
        db.refresh(borrowed)
        return book

@router.get("/users")
def get_users(request: Request , name : str = ""):
    if request.state.user.get("role") != "librarian":
        raise HTTPException(status_code=403, detail="User is not a librarian")
    return LibrarianService.get_all_users(name)


class PDFRequest(pydantic.BaseModel):
    title: str
    reader_id: int = 0
    reader_name: str = ""
    reader_email: str = ""
    borrow_date: str
    return_date: str

@router.post("/generate_pdf")
def generate_pdf(request: Request, pdf_req: PDFRequest):
    data = request.state.user.copy()
    data.update(pdf_req.dict())
    pdf_bytes = LibrarianService.generate_pdf(data)
    return Response(content=pdf_bytes, media_type="application/pdf")
