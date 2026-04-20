import domain.Borrowed as Borrowed
from config.dbConfig import get_db

def get_all_borrowed(page : int , limit : int , sort_by : str , sort_order : str):
    db = get_db()
    return db.query(Borrowed.Borrowed).offset((page - 1) * limit).limit(limit).order_by(getattr(Borrowed.Borrowed, sort_by), sort_order).all()

def get_borrowed(id : int):
    db = get_db()
    return db.query(Borrowed.Borrowed).filter(Borrowed.Borrowed.id == id).first()

def get_borrowed_by_reader(reader_id : int , page : int , limit : int , sort_by : str , sort_order : str):
    db = get_db()
    return db.query(Borrowed.Borrowed).filter(Borrowed.Borrowed.reader_id == reader_id).offset((page - 1) * limit).limit(limit).order_by(getattr(Borrowed.Borrowed, sort_by), sort_order).all()

def get_borrowed_by_librarian(librarian_id : int , page : int , limit : int , sort_by : str , sort_order : str):
    db = get_db()
    return db.query(Borrowed.Borrowed).filter(Borrowed.Borrowed.librarian_id == librarian_id).offset((page - 1) * limit).limit(limit).order_by(getattr(Borrowed.Borrowed, sort_by), sort_order).all()

def get_borrowed_by_book(book_id : int , page : int , limit : int , sort_by : str , sort_order : str):
    db = get_db()
    return db.query(Borrowed.Borrowed).filter(Borrowed.Borrowed.book_id == book_id).offset((page - 1) * limit).limit(limit).order_by(getattr(Borrowed.Borrowed, sort_by), sort_order).all()

def get_borrowed_by_borrow_date(borrow_date : str , page : int , limit : int , sort_by : str , sort_order : str):
    db = get_db()
    return db.query(Borrowed.Borrowed).filter(Borrowed.Borrowed.borrow_date == borrow_date).offset((page - 1) * limit).limit(limit).order_by(getattr(Borrowed.Borrowed, sort_by), sort_order).all()

def get_borrowed_by_return_date(return_date : str , page : int , limit : int , sort_by : str , sort_order : str):
    db = get_db()
    return db.query(Borrowed.Borrowed).filter(Borrowed.Borrowed.return_date == return_date).offset((page - 1) * limit).limit(limit).order_by(getattr(Borrowed.Borrowed, sort_by), sort_order).all()


def create_borrowed(borrowed: Borrowed.BorrowedCreate):
    db = get_db()
    db.add(borrowed)
    db.commit()
    db.refresh(borrowed)
    return Borrowed.Borrowed(**borrowed.dict())

def update_borrowed(borrowed: Borrowed.BorrowedUpdate):
    db = get_db()
    db.merge(borrowed)
    db.commit()
    db.refresh(borrowed)
    return Borrowed.Borrowed(**borrowed.dict())

def delete_borrowed(borrowed: Borrowed.BorrowedDelete):
    db = get_db()
    db.delete(borrowed)
    db.commit()
    return Borrowed.Borrowed(**borrowed.dict())