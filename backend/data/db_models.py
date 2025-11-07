import uuid
from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import CheckConstraint
from enum import IntEnum


class ReceiptScanMethod(IntEnum):
    OCR = 0  # receipt photo ocr -> llm
    QR_CODE = 1  # receipt qr code


class ReceiptItemCategory(IntEnum):
    NOT_CLASSIFIED = 0
    GROCERIES = 1
    DINING_OUT = 2
    TRANSPORTATION = 3
    HOUSING = 4
    UTILITIES = 5
    INTERNET_TV_PHONE = 6
    HEALTHCARE = 7
    PERSONAL_CARE = 8
    CLOTHING = 9
    ENTERTAINMENT = 10
    EDUCATION = 11
    GIFTS_DONATIONS = 12
    TRAVEL = 13
    FINANCIAL_FEES = 14
    HOUSEHOLD_SUPPLIES = 15
    TECHNOLOGY = 16
    PET_CARE = 17
    CHILDCARE = 18
    SPORTS_FITNESS = 19
    OTHER = 99


class User(SQLModel, table=True):
    __tablename__ = "users"
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_id: str = Field(index=True)  # telegram provided uid
    passphrase: str

    receipts: List["Receipt"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )


class Receipt(SQLModel, table=True):
    __tablename__ = "receipts"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    merchant_name: str
    total_amount_cents: int
    currency: str = Field(max_length=10)
    time_stamp: datetime = Field(default_factory=datetime.now)
    receipt_lq_image_path: Optional[str] = Field(default=None, nullable=True)
    user_id: str = Field(foreign_key="users.id", index=True)  # telegram provided uid

    items: List["ReceiptItem"] = Relationship(
        back_populates="receipts",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    operation_metadata: Optional["ReceiptMetadata"] = Relationship(
        back_populates="receipts",
        sa_relationship_kwargs={"uselist": False, "cascade": "all, delete-orphan"},
    )


class ReceiptMetadata(SQLModel, table=True):
    __tablename__ = "receipt_metadata"
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    address: Optional[str] = Field(default=None, nullable=True)
    tax_id: Optional[str] = Field(default=None, nullable=True)
    cashier: Optional[str] = Field(default=None, nullable=True)
    payment_method: Optional[str] = Field(default=None, nullable=True)

    receipt_id: str = Field(foreign_key="receipts.id", ondelete="CASCADE")
    receipt: "Receipt" = Relationship(back_populates="operation_metadata")


class ReceiptItem(SQLModel, table=True):
    __tablename__ = "receipt_items"
    __table_args__ = (
        CheckConstraint("quantity > 0", name="check_quantity_positive"),
        CheckConstraint("unit_price_cents > 0", name="check_unit_price_positive"),
        CheckConstraint("total_price_cents > 0", name="check_total_price_positive"),
    )

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    name: str
    quantity: int
    unit_price_cents: int
    total_price_cents: int
    category: ReceiptItemCategory = Field(default=ReceiptItemCategory.NOT_CLASSIFIED)

    receipt_id: str = Field(foreign_key="receipts.id", ondelete="CASCADE")
    receipt: "Receipt" = Relationship(back_populates="items")
