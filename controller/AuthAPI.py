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
    print(f"AuthAPI: Received login request for {user}")
    return AuthService.loginLibrarian(user)

@router.get("/current-user")
def current_user(user = Depends(AuthService.get_current_user)):
    return user

@router.put("/update-user")
def update_user(user_update: User.UserUpdate, user = Depends(AuthService.get_current_user)):
    return AuthService.update_user(user["id"], user_update)

