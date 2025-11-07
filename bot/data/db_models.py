import uuid
from sqlmodel import SQLModel, Field
from datetime import datetime
from enum import Enum


class ReceiptStatus(str, Enum):
    PENDING = "pending"
    RETRYING = "retrying"
    UPLOADED = "uploaded"
    FAILED = "failed"


class Receipt(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    filename: str
    filepath: str
    uid: str
    timestamp: datetime = Field(default_factory=datetime.now)
    status: ReceiptStatus = Field(default=ReceiptStatus.PENDING)
