import os

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from aio_pika import connect_robust

# load_dotenv()

# Database configuration
DATABASE_URL = os.getenv("DATABASE_URL")
ASYNC_DATABASE_URL = os.getenv("ASYNC_DATABASE_URL")

assert DATABASE_URL is not None, "DATABASE_URL environment variable is not set"
assert ASYNC_DATABASE_URL is not None, (
    "ASYNC_DATABASE_URL environment variable is not set"
)

# Synchronous engine for migrations and initial setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Asynchronous engine for FastAPI
async_engine = create_async_engine(ASYNC_DATABASE_URL)
async_session = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)  # type: ignore


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


# Message queue configuration
RABBIT_MQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost/")


async def get_message_queue():
    """Dependency to get message queue connection"""

    connection = await connect_robust(RABBIT_MQ_URL)
    try:
        yield connection
    finally:
        await connection.close()
