import fastapi
from controller.AuthAPI import router as auth_app
from controller.BooksApi import router as books_app
from controller.ReaderApi import router as reader_app
from controller.LibrarianAPI import router as librarian_app
from service.auth.authMiddelware import JWTMiddleware


app = fastapi.FastAPI()

app.add_middleware(JWTMiddleware)
app.include_router(auth_app)
app.include_router(books_app)
app.include_router(reader_app)
app.include_router(librarian_app)


