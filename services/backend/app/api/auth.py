from fastapi import APIRouter, HTTPException, status, Header
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse

router = APIRouter()

_users: dict[str, str] = {}

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest):
    email = payload.email.lower()
    if email in _users:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    _users[email] = payload.password
    return {"message": "registered"}

@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest):
    email = payload.email.lower()
    if _users.get(email) != payload.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return TokenResponse(access_token="dev-token")

@router.post("/logout")
def logout():
    return {"message": "logged out"}

@router.get("/me")
def me(authorization: str | None = Header(default=None)):
    # Minimal check: expects "Bearer dev-token"
    if authorization != "Bearer dev-token":
        return {"authenticated": False}
    return {"authenticated": True}
