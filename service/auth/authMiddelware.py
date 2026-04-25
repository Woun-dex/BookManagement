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
        token = None
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
        else:
            token = request.cookies.get("token")

        path = request.url.path.rstrip("/").lower()
        if not path:
            path = "/"

        excluded_paths = [p.lower() for p in ["/docs", "/openapi.json", "/login", "/register", "/loginLibrarian"]]

        if request.method == "OPTIONS" or any(path.endswith(p) for p in excluded_paths):
            return await call_next(request)

        if not token:
            print(f"JWTMiddleware: returning 401 because token is {token}")
            return JSONResponse(
                status_code=401, 
                content={"detail": "Missing or invalid token"}
            )

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