import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()
# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://localhost/inventory_db")
ASYNC_DATABASE_URL = os.getenv(
    "ASYNC_DATABASE_URL", "postgresql+asyncpg://localhost/inventory_db"
)

# Synchronous engine for migrations and initial setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Asynchronous engine for FastAPI
async_engine = create_async_engine(ASYNC_DATABASE_URL)
async_session = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)  # type: ignore

Base = declarative_base()


def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_async_db():
    """Dependency to get async database session"""
    async with async_session() as session:  # type: ignore
        yield session
