from data import CalculationPeriod
from tools import period_to_daterange
from core import logger
from data.repositories import ExpensesRepository, UserRepository, ReceiptRepository
from data import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime


class UsersExpensesJob:
    def __init__(
        self,
        session: AsyncSession,
    ):
        self.user_repo = UserRepository(session)
        self.receipt_repo = ReceiptRepository(session)
        self.expenses_repo = ExpensesRepository(session)

    async def for_all_users(self, period: CalculationPeriod) -> None:
        users = await self.user_repo.get_all()
        for user in users:
            await self.for_user(user_id=user.id, period=period)

    async def for_user(self, user_id: str, period: CalculationPeriod) -> bool:
        logger.info(f"Start calculate user {user_id} expenses for period {period}.")
        now = datetime.now()
        start, end = period_to_daterange(period)
        try:
            summary = await self.expenses_repo.get_summary(user_id, period, start)

            if summary and summary.calculated_at:
                calc_start = summary.calculated_at.date()
            else:
                calc_start = start

            if calc_start >= end:
                return True

            new_total_cents = await self.receipt_repo.get_total_spending(
                user_id, start_date=calc_start, end_date=now
            )

            total_cents = new_total_cents + (
                summary.total_expense_cents if summary else 0
            )

            await self.expenses_repo.upsert_summary(
                user_id,
                period_type=period,
                period_start=start,
                period_end=end,
                total_expense_cents=total_cents,
            )

            logger.info(
                f"Successfully calculated user {user_id} expenses for period {period}."
            )
            return True

        except Exception as e:
            logger.error(
                f"Failed to calculate period {period} expenses for user {user_id}."
                f"Exception: {e}"
            )
            return False


async def run_user_expenses(calculation_period: CalculationPeriod):
    async with get_session() as session:
        job = UsersExpensesJob(session)
        await job.for_all_users(calculation_period)


async def run_for_user(user_id: str):
    async with get_session() as session:
        job = UsersExpensesJob(session)
        for period in CalculationPeriod:
            await job.for_user(user_id, period)


async def run_for_all(user_id: str):
    async with get_session() as session:
        job = UsersExpensesJob(session)
        for period in CalculationPeriod:
            await job.for_all_users(user_id, period)
