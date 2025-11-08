from typing import List, Optional

from models.receipt import LineItem, Receipt, ReceiptMetadata
from data.db_models import (
    DbReceipt,
    DbReceiptItem,
    DbReceiptMetadata,
)


class ReceiptMapper:
    """Converts Pydantic receipt models to SQLModel database models"""

    @staticmethod
    def dollars_to_cents(amount: float) -> int:
        """Convert dollar amount to cents"""
        return int(round(amount * 100))

    @staticmethod
    def cents_to_dollars(cents: int) -> float:
        """Convert cents to dollar amount"""
        return cents / 100.0

    @classmethod
    def pydantic_to_db_receipt(
        cls,
        pydantic_receipt: Receipt,
        user_id: str,
        receipt_image_path: Optional[str] = None,
    ) -> DbReceipt:
        """
        Convert Pydantic Receipt to SQLModel Receipt

        Args:
            pydantic_receipt: Parsed receipt from LLM
            user_id: User's internal UUID (from User table)
            receipt_image_path: Path to stored receipt image

        Returns:
            DBReceipt ready to be added to session
        """
        db_receipt = DbReceipt(
            merchant_name=pydantic_receipt.merchant_name or "Unknown Merchant",
            total_amount_cents=cls.dollars_to_cents(pydantic_receipt.total_amount),
            currency=pydantic_receipt.currency,
            receipt_lq_image_path=receipt_image_path,
            user_id=user_id,
        )

        return db_receipt

    @classmethod
    def pydantic_to_db_items(
        cls, line_items: List[LineItem], receipt_id: str
    ) -> List[DbReceiptItem]:
        """
        Convert Pydantic LineItems to SQLModel ReceiptItems

        Args:
            line_items: List of parsed line items
            receipt_id: ID of the parent receipt

        Returns:
            List of DBReceiptItem ready to be added to session
        """
        db_items = []

        for item in line_items:
            db_item = DbReceiptItem(
                name=item.name,
                quantity=item.quantity,
                unit_price_cents=cls.dollars_to_cents(item.unit_price),
                total_price_cents=cls.dollars_to_cents(item.total_price),
                receipt_id=receipt_id,
            )
            db_items.append(db_item)

        return db_items

    @classmethod
    def pydantic_to_db_metadata(
        cls, pydantic_metadata: ReceiptMetadata, receipt_id: str
    ) -> Optional[DbReceiptMetadata]:
        """
        Convert Pydantic ReceiptMetadata to SQLModel ReceiptMetadata

        Args:
            pydantic_metadata: Parsed metadata from LLM
            receipt_id: ID of the parent receipt

        Returns:
            DBReceiptMetadata or None if no metadata provided
        """
        # Only create metadata if at least one field is present
        if not any(
            [
                pydantic_metadata.address,
                pydantic_metadata.tax_id,
                pydantic_metadata.cashier,
                pydantic_metadata.payment_method,
            ]
        ):
            return None

        db_metadata = DbReceiptMetadata(
            address=pydantic_metadata.address,
            tax_id=pydantic_metadata.tax_id,
            cashier=pydantic_metadata.cashier,
            payment_method=pydantic_metadata.payment_method,
            receipt_id=receipt_id,
        )

        return db_metadata

    @classmethod
    def convert_complete_receipt(
        cls,
        pydantic_receipt: Receipt,
        user_id: str,
        receipt_image_path: Optional[str] = None,
    ) -> DbReceipt:
        """
        Convert complete Pydantic receipt to database models

        Args:
            pydantic_receipt: Parsed receipt
            user_id: User's internal UUID
            receipt_image_path: Path to stored receipt image

        Returns:
            Tuple of (DBReceipt, List[DBReceiptItem], Optional[DBReceiptMetadata])
        """

        db_receipt = cls.pydantic_to_db_receipt(
            pydantic_receipt, user_id, receipt_image_path
        )

        db_receipt.items = cls.pydantic_to_db_items(
            pydantic_receipt.line_items,
            db_receipt.id,
        )

        db_receipt.operation_metadata = cls.pydantic_to_db_metadata(
            pydantic_receipt.metadata, db_receipt.id
        )

        return db_receipt
