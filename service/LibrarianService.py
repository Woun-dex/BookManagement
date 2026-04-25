import domain.Borrowed as Borrowed
import service.PdfGenerator as PdfGenerator
import domain.Books as Books
from config.dbConfig import get_db

def get_all_borrowed(page : int , limit : int , sort_by : str , sort_order : str):
    db = next(get_db())
    col = getattr(Borrowed.Borrowed, sort_by)
    order_expr = col.desc() if sort_order.lower() == "desc" else col.asc()
    
    results = db.query(Borrowed.Borrowed, Books.Book.title).join(
        Books.Book, Borrowed.Borrowed.book_id == Books.Book.id
    ).order_by(order_expr).offset((page - 1) * limit).limit(limit).all()
    
    formatted_results = []
    for borrowed, book_title in results:
        borrowed_dict = {k: v for k, v in borrowed.__dict__.items() if not k.startswith('_')}
        borrowed_dict["book_name"] = book_title
        formatted_results.append(borrowed_dict)
        
    return formatted_results

def get_borrowed(id : int):
    db = next(get_db())
    return db.query(Borrowed.Borrowed).filter(Borrowed.Borrowed.id == id).first()

def get_borrowed_by_reader(reader_id : int , page : int , limit : int , sort_by : str , sort_order : str):
    db = next(get_db())
    col = getattr(Borrowed.Borrowed, sort_by)
    order_expr = col.desc() if sort_order.lower() == "desc" else col.asc()
    return db.query(Borrowed.Borrowed).filter(Borrowed.Borrowed.reader_id == reader_id).order_by(order_expr).offset((page - 1) * limit).limit(limit).all()

def get_borrowed_by_librarian(librarian_id : int , page : int , limit : int , sort_by : str , sort_order : str):
    db = next(get_db())
    col = getattr(Borrowed.Borrowed, sort_by)
    order_expr = col.desc() if sort_order.lower() == "desc" else col.asc()

    results = db.query(Borrowed.Borrowed, Books.Book).join(
        Books.Book, Borrowed.Borrowed.book_id == Books.Book.id
    ).filter(Borrowed.Borrowed.librarian_id == librarian_id).order_by(order_expr).offset((page - 1) * limit).limit(limit).all()
    
    formatted_results = []
    for borrowed, book in results:
        borrowed_dict = {k: v for k, v in borrowed.__dict__.items() if not k.startswith('_')}
        borrowed_dict["book"] = book
        formatted_results.append(borrowed_dict)
        
    return formatted_results

def get_borrowed_by_book(book_id : int , page : int , limit : int , sort_by : str , sort_order : str):
    db = next(get_db())
    col = getattr(Borrowed.Borrowed, sort_by)
    order_expr = col.desc() if sort_order.lower() == "desc" else col.asc()
    return db.query(Borrowed.Borrowed).filter(Borrowed.Borrowed.book_id == book_id).order_by(order_expr).offset((page - 1) * limit).limit(limit).all()

def get_borrowed_by_borrow_date(borrow_date : str , page : int , limit : int , sort_by : str , sort_order : str):
    db = next(get_db())
    col = getattr(Borrowed.Borrowed, sort_by)
    order_expr = col.desc() if sort_order.lower() == "desc" else col.asc()
    return db.query(Borrowed.Borrowed).filter(Borrowed.Borrowed.borrow_date == borrow_date).order_by(order_expr).offset((page - 1) * limit).limit(limit).all()

def get_borrowed_by_return_date(return_date : str , page : int , limit : int , sort_by : str , sort_order : str):
    db = next(get_db())
    col = getattr(Borrowed.Borrowed, sort_by)
    order_expr = col.desc() if sort_order.lower() == "desc" else col.asc()
    return db.query(Borrowed.Borrowed).filter(Borrowed.Borrowed.return_date == return_date).order_by(order_expr).offset((page - 1) * limit).limit(limit).all()


def create_borrowed(borrowed: Borrowed.BorrowedCreate):
    db = next(get_db())
    new_borrowed = Borrowed.Borrowed(**borrowed.dict())
    db.add(new_borrowed)
    db.commit()
    db.refresh(new_borrowed)
    return new_borrowed

def update_borrowed(borrowed: Borrowed.BorrowedUpdate):
    db = next(get_db())
    updated_borrowed = Borrowed.Borrowed(**borrowed.dict())
    db.merge(updated_borrowed)
    db.commit()
    return updated_borrowed

def delete_borrowed(borrowed: Borrowed.BorrowedDelete):
    db = next(get_db())
    borrowed_to_delete = db.query(Borrowed.Borrowed).filter(Borrowed.Borrowed.id == borrowed.id).first()
    if borrowed_to_delete:
        db.delete(borrowed_to_delete)
        db.commit()
    return borrowed_to_delete

def get_all_users(name : str):
    db = next(get_db())
    return db.query(User.User).filter(User.User.name.like(f"%{name}%")).all()


def generate_pdf(data):
    return PdfGenerator.generate_pdf(data)