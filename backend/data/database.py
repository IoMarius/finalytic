import os
from .db_models import SQLModel
from sqlmodel import create_engine, Session
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from typing import AsyncGenerator

from contextlib import asynccontextmanager
from sqlalchemy.orm import sessionmaker

DATABASE_URL = (
    f"postgresql+asyncpg://"
    f"{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
    f"@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}"
    f"/{os.getenv('POSTGRES_DB')}"
)

engine = create_async_engine(
    DATABASE_URL,
    echo=os.getenv("PRINT_SQL_STATEMENTS", "False").lower() == "true",
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
)
async_session_factory = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)


async def init_db():
    from .db_models import DbUser, DbReceipt, DbReceiptItem, DbReceiptMetadata

    print("[DB] Start create database tables")
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
    # SQLModel.metadata.create_all(engine)
    print("[DB] Database tables created successfully")


# @contextmanager
# def get_session():
#     with AsyncSession(engine) as session:
#         yield session

@asynccontextmanager
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        yield session
