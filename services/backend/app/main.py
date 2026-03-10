from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.auth import router as auth_router
from app.api.health import router as health_router
from app.api.profiles import router as profiles_router
from app.api.integration import profile_router

app = FastAPI(title="Chronicle API", version="0.1.0")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, prefix="/api", tags=["health"])
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(profiles_router, prefix="/api/user-profile", tags=["user-profile"])
app.include_router(profile_router, prefix="/api/profile", tags=["calendar-profile"])
