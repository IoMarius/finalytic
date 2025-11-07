import uuid
from sqlmodel import SQLModel, Field
from datetime import datetime
from enum import IntEnum


class ReceiptUploadStatus(IntEnum):
    PENDING = 0
    RETRYING = 1
    UPLOADED = 2
    FAILED = 3


class Receipt(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    filename: str
    filepath: str
    uid: str
    timestamp: datetime = Field(default_factory=datetime.now)
    status: ReceiptUploadStatus = Field(default=ReceiptUploadStatus.PENDING)
