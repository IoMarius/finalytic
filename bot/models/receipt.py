from pydantic import BaseModel
from typing import Generic, Optional, TypeVar


T = TypeVar("T")


class APIResponse(BaseModel, Generic[T]):
    """Standardized API response wrapper"""

    success: bool = False
    data: Optional[T] = None
    message: Optional[str]


# class ReceiptSummary(BaseModel):
#     """API response from receipt processing"""

#     merchant_name: Optional[str] = None
#     total_amount: float
#     currency: str
