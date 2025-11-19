# from sqlalchemy import insert
from datetime import datetime
from typing import List

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select, and_

from data import CalculationPeriod, DbUserExpenseSummary
from data.repositories import BaseRepository


class ExpensesRepository(BaseRepository[DbUserExpenseSummary]):

    def __init__(self, session: AsyncSession):
        super().__init__(DbUserExpenseSummary, session)

    async def get_user_expenses(
        self,
        user_id: str,
        period_type: CalculationPeriod,
        skip: int = 0,
        limit: int = 100,
    ) -> List[DbUserExpenseSummary]:
        statement = (
            select(DbUserExpenseSummary)
            .where(DbUserExpenseSummary.user_id == user_id)
            .where(DbUserExpenseSummary.period_type == period_type)
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(statement)
        return result.scalars().all()

    async def upsert_summary(
        self,
        user_id: str,
        period_type: CalculationPeriod,
        period_start: datetime,
        period_end: datetime,
        total_expense_cents: int,
    ) -> None:
        stmt = insert(DbUserExpenseSummary).values(
            user_id=user_id,
            period_type=period_type,
            period_start=period_start,
            period_end=period_end,
            total_expense_cents=total_expense_cents,
            calculated_at=datetime.now(),
        )

        stmt = stmt.on_conflict_do_update(
            index_elements=[
                DbUserExpenseSummary.user_id,
                DbUserExpenseSummary.period_type,
                DbUserExpenseSummary.period_start,
                DbUserExpenseSummary.period_end,
            ],
            set_={
                "total_expense_cents": stmt.excluded.total_expense_cents,
                "calculated_at": datetime.now(),
            },
        )

        await self.session.execute(stmt)
        await self.session.commit()

    async def get_summary(
        self, user_id: str, period: CalculationPeriod, period_start: datetime
    ) -> DbUserExpenseSummary:
        # statement = (
        #     select(DbUserExpenseSummary)
        #     .where(DbUserExpenseSummary.user_id == user_id)
        #     .where(DbUserExpenseSummary.period_type == period)
        #     .where(DbUserExpenseSummary.period_start == period_start)
        # )
        summary = await self.session.scalar(
            select(DbUserExpenseSummary)
            .where(DbUserExpenseSummary.user_id == user_id)
            .where(DbUserExpenseSummary.period_type == period)
            .where(DbUserExpenseSummary.period_start == period_start)
        )
        # return result.scalars().all()
        return summary
