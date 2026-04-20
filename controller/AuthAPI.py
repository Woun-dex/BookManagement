import fastapi
from fastapi import Depends
import service.auth.authService as AuthService
import domain.user as User
from service.auth.authMiddelware import JWTMiddleware



router = fastapi.APIRouter()


@router.post("/register")
def register(user: User.UserCreate):
    return AuthService.register(user)

@router.post("/login")
def login(user: User.UserLogin):
    return AuthService.login(user)

@router.post("/loginLibrarian")
def loginLibrarian(user: User.UserLogin):
    return AuthService.loginLibrarian(user)

@router.get("/current_user")
def current_user(token: str = Depends(AuthService.get_current_user)):
    return token

