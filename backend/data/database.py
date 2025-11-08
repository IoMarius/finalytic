import os
from sqlmodel import create_engine, Session
from .db_models import SQLModel
from contextlib import contextmanager
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

DATABASE_URL = (
    f"postgresql+psycopg2://"
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


def init_db():
    from .db_models import DbUser, DbReceipt, DbReceiptItem, DbReceiptMetadata

    print("[DB] Start create database tables")
    SQLModel.metadata.create_all(engine)
    print("[DB] Database tables created successfully")


@contextmanager
def get_session():
    with AsyncSession(engine) as session:
        yield session
