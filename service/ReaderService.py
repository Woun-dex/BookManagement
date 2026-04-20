import domain.user as User
from config.dbConfig import get_db

def get_all_readers(page: int, limit: int , sort_by: str , sort_order: str):
    db = get_db()
    return db.query(User.User).offset((page - 1) * limit).limit(limit).order_by(getattr(User.User, sort_by), sort_order).all() 

def get_reader(id: int):
    db = get_db()
    return db.query(User.User).filter(User.User.id == id).first()

def get_reader_by_name(name: str , page : int , limit : int):
    db = get_db()
    return db.query(User.User).filter(User.User.full_name == name).offset((page - 1) * limit).limit(limit).all()

def get_reader_by_email(email: str , page : int , limit : int):
    db = get_db()
    return db.query(User.User).filter(User.User.email == email).offset((page - 1) * limit).limit(limit).all()

def create_reader(reader: User.UserCreate):
    db = get_db()
    new_reader = User.User(**reader.dict())
    db.add(new_reader)
    db.commit()
    db.refresh(new_reader)
    return new_reader

def update_reader(reader: User.UserUpdate):
    db = get_db()
    updated_reader = User.User(**reader.dict())
    db.merge(updated_reader)
    db.commit()
    return updated_reader

def delete_reader(reader: User.UserDelete):
    db = get_db()
    db.delete(reader)
    db.commit()
    return reader