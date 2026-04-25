import domain.user as User
from config.dbConfig import get_db_session

def get_all_readers(page: int, limit: int , sort_by: str , sort_order: str):
    with get_db_session() as db:
        col = getattr(User.User, sort_by)
        order_expr = col.desc() if sort_order.lower() == "desc" else col.asc()
        return db.query(User.User).order_by(order_expr).offset((page - 1) * limit).limit(limit).all() 

def get_reader(id: int):
    with get_db_session() as db:
        return db.query(User.User).filter(User.User.id == id).first()

def get_reader_by_name(name: str , page : int , limit : int):
    with get_db_session() as db:
        return db.query(User.User).filter(User.User.full_name == name).offset((page - 1) * limit).limit(limit).all()

def get_reader_by_email(email: str , page : int , limit : int):
    with get_db_session() as db:
        return db.query(User.User).filter(User.User.email == email).offset((page - 1) * limit).limit(limit).all()

def create_reader(reader: User.UserCreate):
    with get_db_session() as db:
        new_reader = User.User(**reader.dict())
        db.add(new_reader)
        db.commit()
        db.refresh(new_reader)
        return new_reader

def update_reader(reader: User.UserUpdate):
    with get_db_session() as db:
        updated_reader = User.User(**reader.dict())
        db.merge(updated_reader)
        db.commit()
        return updated_reader

def delete_reader(reader: User.UserDelete):
    with get_db_session() as db:
        db.delete(reader)
        db.commit()
        return reader