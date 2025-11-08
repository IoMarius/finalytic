from pydantic import BaseModel, Field, field_validator
from typing import Generic, Optional, List, TypeVar

from data.db_models import ReceiptItemCategory

T = TypeVar("T")


class APIResponse(BaseModel, Generic[T]):
    """Standardized API response wrapper"""

    success: bool = False
    data: Optional[T] = None
    message: Optional[str] = None


class LineItem(BaseModel):
    """Individual line item from receipt"""

    name: str
    quantity: float = Field(gt=0, description="Quantity must be greater than 0")
    unit_price: float = Field(ge=0, description="Unit price must be non-negative")
    total_price: float = Field(ge=0, description="Total price must be non-negative")

    @field_validator("total_price")
    @classmethod
    def validate_total(cls, v, info):
        """Optionally validate that total = quantity * unit_price"""
        """Optionally validate that total = quantity * unit_price"""
        # You can enable this validation if needed
        quantity = info.data.get("quantity")
        unit_price = info.data.get("unit_price")
        if quantity and unit_price:
            expected = round(quantity * unit_price, 2)
            if abs(v - expected) > 0.01:
                raise ValueError(
                    f"Total price {v} does not match quantity * unit_price"
                )
        return v


class ReceiptMetadata(BaseModel):
    """Additional receipt metadata"""

    address: Optional[str] = None
    tax_id: Optional[str] = None
    cashier: Optional[str] = None
    payment_method: Optional[str] = None


class Receipt(BaseModel):
    """Complete receipt structure"""

    merchant_name: Optional[str] = None
    total_amount: float = Field(ge=0, description="Total amount must be non-negative")
    currency: str = Field(min_length=1, description="Currency code cannot be empty")
    line_items: List[LineItem] = Field(
        min_length=1, description="Must have at least one line item"
    )
    metadata: ReceiptMetadata

    @field_validator("currency")
    @classmethod
    def validate_currency(cls, v):
        """Ensure currency is uppercase"""
        return v.upper()

    @field_validator("line_items")
    @classmethod
    def validate_line_items_total(cls, v, info):
        """Optionally validate that line items sum to total_amount"""
        # You can enable this validation if needed
        total_amount = info.data.get("total_amount")
        if total_amount:
            items_sum = sum(item.total_price for item in v)
            if abs(items_sum - total_amount) > 0.01:
                raise ValueError(
                    f"Line items sum {items_sum} does not match total_amount {total_amount}"
                )
        return v


class ReceiptSummary(BaseModel):
    """API response from receipt processing"""

    merchant_name: Optional[str] = None
    total_amount: float
    currency: str
    total_items: int


class CategorizedReceiptItem(BaseModel):
    row_id: str
    name: str
    category: Optional[ReceiptItemCategory] = None
