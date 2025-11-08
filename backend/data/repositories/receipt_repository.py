from typing import List, Optional
from datetime import datetime
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, and_
from ..db_models import DbReceipt, DbReceiptItem, DbReceiptMetadata, ReceiptItemCategory
from .base_repository import BaseRepository


class ReceiptRepository(BaseRepository[DbReceipt]):

    def __init__(self, session: AsyncSession):
        super().__init__(DbReceipt, session)

    async def get_user_receipts(
        self, user_id: str, skip: int = 0, limit: int = 100
    ) -> List[DbReceipt]:
        statement = (
            select(DbReceipt)
            .where(DbReceipt.user_id == user_id)
            .order_by(DbReceipt.time_stamp.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(statement)
        return result.scalars().all()

    async def get_receipts_by_date_range(
        self, user_id: str, start_date: datetime, end_date: datetime
    ) -> List[DbReceipt]:
        statement = (
            select(DbReceipt)
            .where(
                and_(
                    DbReceipt.user_id == user_id,
                    DbReceipt.time_stamp >= start_date,
                    DbReceipt.time_stamp <= end_date,
                )
            )
            .order_by(DbReceipt.time_stamp.desc())
        )
        result = await self.session.execute(statement)
        return result.scalars().all()

    async def get_receipts_by_merchant(
        self, user_id: str, merchant_name: str
    ) -> List[DbReceipt]:
        statement = (
            select(DbReceipt)
            .where(
                and_(
                    DbReceipt.user_id == user_id,
                    DbReceipt.merchant_name.ilike(f"%{merchant_name}%"),
                )
            )
            .order_by(DbReceipt.time_stamp.desc())
        )
        result = await self.session.execute(statement)
        return result.scalars().all()

    async def create_receipt_with_items(
        self,
        user_id: str,
        merchant_name: str,
        total_amount_cents: int,
        currency: str,
        items: List[dict],
        metadata: Optional[dict] = None,
        receipt_image_path: Optional[str] = None,
    ) -> DbReceipt:
        receipt = DbReceipt(
            user_id=user_id,
            merchant_name=merchant_name,
            total_amount_cents=total_amount_cents,
            currency=currency,
            receipt_lq_image_path=receipt_image_path,
        )

        self.session.add(receipt)
        await self.session.flush()  # async flush

        for item_data in items:
            item = DbReceiptItem(
                receipt_id=receipt.id,
                name=item_data["name"],
                quantity=item_data["quantity"],
                unit_price_cents=item_data["unit_price_cents"],
                total_price_cents=item_data["total_price_cents"],
                category=item_data.get("category", ReceiptItemCategory.NOT_CLASSIFIED),
            )
            self.session.add(item)

        if metadata:
            receipt_metadata = DbReceiptMetadata(
                receipt_id=receipt.id,
                address=metadata.get("address"),
                tax_id=metadata.get("tax_id"),
                cashier=metadata.get("cashier"),
                payment_method=metadata.get("payment_method"),
            )
            self.session.add(receipt_metadata)

        await self.session.commit()
        await self.session.refresh(receipt)
        return receipt

    async def get_total_spending(
        self,
        user_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> int:
        statement = select(DbReceipt).where(DbReceipt.user_id == user_id)

        if start_date:
            statement = statement.where(DbReceipt.time_stamp >= start_date)
        if end_date:
            statement = statement.where(DbReceipt.time_stamp <= end_date)

        result = await self.session.execute(statement)
        receipts = result.scalars().all()
        return sum(r.total_amount_cents for r in receipts)

    async def get_spending_by_category(
        self,
        user_id: str,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
    ) -> dict:
        statement = (
            select(
                DbReceiptItem.category,
                func.sum(DbReceiptItem.total_price_cents).label("total"),
            )
            .join(DbReceipt)
            .where(DbReceipt.user_id == user_id)
            .group_by(DbReceiptItem.category)
        )

        if start_date:
            statement = statement.where(DbReceipt.time_stamp >= start_date)
        if end_date:
            statement = statement.where(DbReceipt.time_stamp <= end_date)

        result = await self.session.execute(statement)
        rows = result.all()
        return {ReceiptItemCategory(category).name: total for category, total in rows}
