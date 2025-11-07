import uuid
from sqlmodel import SQLModel, Field
from datetime import datetime
from enum import Enum

class ReceiptItem(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    name: str
    quantity: int
    unit_price: float
    total_price: float
    