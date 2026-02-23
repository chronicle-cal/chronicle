from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.auth import router as auth_router
from app.api.health import router as health_router
from app.api.profiles import router as profiles_router
from app.core.db import Base, engine

app = FastAPI(title="Chronicle API", version="0.1.0")


@app.on_event("startup")
async def create_missing_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # statt "*"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health auch unter /api (optional, aber konsistent)
app.include_router(health_router, prefix="/api", tags=["health"])
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(profiles_router, prefix="/api/profiles", tags=["profiles"])
