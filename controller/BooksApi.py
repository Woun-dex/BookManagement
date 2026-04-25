import fastapi
import pydantic
from fastapi import APIRouter , Depends , HTTPException , Request
import service.BooksService as BooksService
import domain.Books as Book

router = APIRouter()

@router.get("/books")
def get_all_books(request: Request , page : int = 1 , limit : int = 10 , sort_by : str = "id" , sort_order : str = "asc"):
    return BooksService.get_all_books(page , limit , sort_by , sort_order)

@router.get("/books/search")
def search_books(request: Request , query: str = "", page : int = 1 , limit : int = 10 , sort_by : str = "id" , sort_order : str = "asc"):
    return BooksService.search_books(query, page, limit, sort_by, sort_order)


@router.get("/books/title/{title}")
def get_books_by_title(request: Request , title : str , page : int = 1 , limit : int = 10 , sort_by : str = "id" , sort_order : str = "asc"):
    return BooksService.get_books_by_title(title , page , limit , sort_by , sort_order)

@router.get("/books/author/{author}")
def get_books_by_author(request: Request , author : str , page : int = 1 , limit : int = 10 , sort_by : str = "id" , sort_order : str = "asc"):
    return BooksService.get_books_by_author(author , page , limit , sort_by , sort_order)

@router.get("/books/category/{category}")
def get_books_by_category(request: Request , category : str , page : int = 1 , limit : int = 10 , sort_by : str = "id" , sort_order : str = "asc"):
    return BooksService.get_books_by_category(category , page , limit , sort_by , sort_order)

@router.get("/books/{id}")
def get_book(request: Request , id : int):
    return BooksService.get_book(id)

@router.get("/books/rate/{rate}")
def get_books_by_rate(request: Request , rate : int , page : int = 1 , limit : int = 10 , sort_by : str = "id" , sort_order : str = "asc"):
    return BooksService.get_books_by_rate(rate , page , limit , sort_by , sort_order)


@router.post("/books")
def add_book(request: Request, book: Book.BookCreate):
    
    return BooksService.create_book(book)

@router.put("/books")
def update_book(request: Request , book: Book.BookUpdate):
   
    return BooksService.update_book(book)

@router.delete("/books")
def delete_book(request: Request , book: Book.BookDelete):
    return BooksService.delete_book(book)



class BookBriefRequest(pydantic.BaseModel):
    title: str
    author: str
    category: str

@router.post("/books/generate-brief")
def generate_book_brief(request: BookBriefRequest):
    return BooksService.generate_book_brief(request.title , request.author , request.category)
