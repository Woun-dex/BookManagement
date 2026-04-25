import fastapi
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
load_dotenv()

from controller.AuthAPI import router as auth_app
from controller.BooksApi import router as books_app
from controller.ReaderApi import router as reader_app
from controller.LibrarianAPI import router as librarian_app
from controller.UserProfileApi import router as user_profile_app
from service.auth.authMiddelware import JWTMiddleware



app = fastapi.FastAPI()

app.add_middleware(JWTMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth_app)
app.include_router(books_app)
app.include_router(reader_app)
app.include_router(librarian_app)
app.include_router(user_profile_app)

import domain.user as User
import domain.Books as Books
import domain.Borrowed as Borrowed
import domain.BooksRate as BooksRate
import domain.UserProfile as UserProfile
from config.dbConfig import Base, engine

Base.metadata.create_all(bind=engine)
