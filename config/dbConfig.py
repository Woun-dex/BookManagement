from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

POSTGRES_URL = "postgresql://postgres:walid@localhost:5432/book_management"

try:
    import psycopg2
    from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
    from urllib.parse import urlparse
    
    result = urlparse(POSTGRES_URL)
    username = result.username
    password = result.password
    database = result.path[1:]
    hostname = result.hostname
    port = result.port
    
    # Connect to the default 'postgres' database
    connection = psycopg2.connect(
        user=username, 
        password=password, 
        host=hostname, 
        port=port, 
        database="postgres"
    )
    connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = connection.cursor()
    
    # Check if target database exists
    cursor.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{database}'")
    exists = cursor.fetchone()
    if not exists:
        cursor.execute(f"CREATE DATABASE {database}")
    
    cursor.close()
    connection.close()
except Exception as e:
    print(f"Failed to check or create database: {e}")

engine = create_engine(POSTGRES_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

Base.metadata.create_all(bind=engine)