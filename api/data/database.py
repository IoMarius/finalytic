import os
from sqlmodel import create_engine, Session, select
from sqlalchemy import and_
from .db_models import SQLModel
from typing import List

engine = create_engine(
    f"postgresql+psycopg2://{os.getenv("POSTGRES_CONNECTION_STRING")}",
    echo=os.getenv("PRINT_SQL_STATEMENTS"),
)

def init_db():
    SQLModel.metadata.create_all(engine)
