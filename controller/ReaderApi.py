import fastapi
from fastapi import APIRouter , Depends , HTTPException , Request
import service.ReaderService as ReaderService

router = APIRouter()

@router.get("/readers")
def get_all_readers(request: Request , page : int = 1 , limit : int = 10 , sort_by : str = "id" , sort_order : str = "asc"):
    if request.state.user.role != "librarian":
        raise HTTPException(status_code=403, detail="User is not a librarian")
    return ReaderService.get_all_readers(page , limit , sort_by , sort_order)

@router.get("/readers/{id}")
def get_reader(request: Request , id : int):
    if request.state.user.role != "librarian":
        raise HTTPException(status_code=403, detail="User is not a librarian")
    return ReaderService.get_reader(id)

@router.get("/readers/name/{name}")
def get_reader_by_name(request: Request , name : str , page : int = 1 , limit : int = 10 , sort_by : str = "id" , sort_order : str = "asc"):
    if request.state.user.role != "librarian":
        raise HTTPException(status_code=403, detail="User is not a librarian")
    return ReaderService.get_reader_by_name(name , page , limit , sort_by , sort_order)

@router.get("/readers/email/{email}")
def get_reader_by_email(request: Request , email : str , page : int = 1 , limit : int = 10 , sort_by : str = "id" , sort_order : str = "asc"):
    if request.state.user.role != "librarian":
        raise HTTPException(status_code=403, detail="User is not a librarian")
    return ReaderService.get_reader_by_email(email , page , limit , sort_by , sort_order)

