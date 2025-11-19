from data import CalculationPeriod
from tools import period_to_daterange
from core import logger
from data.repositories import ExpensesRepository, UserRepository, ReceiptRepository
from sqlalchemy.ext.asyncio import AsyncSession


class UsersExpensesJob:
    def __init__(
        self,
        session: AsyncSession,
        # user_repo: UserRepository,
        # receipt_repo: ReceiptRepository,
        # expenses_repo: ExpensesRepository,
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
        start, end = period_to_daterange(period)
        try:
            total_cents = await self.receipt_repo.get_total_spending(
                user_id, start_date=start, end_date=end
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
