import fastapi
from fastapi.security import OAuth2PasswordBearer , OAuth2PasswordRequestForm
from fastapi import Depends
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
from fastapi import Request
from service.auth.authHelper import SECRET_KEY, ALGORITHM
import jwt


class JWTMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 1. Get the Authorization header
        auth_header = request.headers.get("Authorization")
        
        # Define paths that don't require authentication
        if request.url.path in ["/docs", "/openapi.json", "/login" , "/register" , "/loginLibrarian"]:
            return await call_next(request)

        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(
                status_code=401, 
                content={"detail": "Missing or invalid token"}
            )

        token = auth_header.split(" ")[1]

        try:
            # 2. Decode the token
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            
            # 3. Store the user info in request state
            request.state.user = payload
            
        except jwt.ExpiredSignatureError:
            return JSONResponse(status_code=401, content={"detail": "Token expired"})
        except jwt.InvalidTokenError:
            return JSONResponse(status_code=401, content={"detail": "Invalid token"})

        # 4. Proceed to the next handler
        response = await call_next(request)
        return response