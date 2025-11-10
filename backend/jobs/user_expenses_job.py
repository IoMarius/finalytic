from services import (
    UserRepository,
    ReceiptRepository,
    CalculationPeriod,
    period_to_daterange,
    logger,
)


class UsersExpensesJob:
    def __init__(self, user_repo: UserRepository, receipt_repo: ReceiptRepository):
        self.user_repo = user_repo
        self.receipt_repo = receipt_repo

    async def for_all_users(self, period: CalculationPeriod) -> None:
        users = await self.user_repo.get_all()

        for user in users:

            self.for_user(user_id=user.id)

    async def for_user(self, user_id: str, period: CalculationPeriod) -> bool:
        logger.info(f"Start calculate user {user_id} expenses for period {period}.")
        start, end = period_to_daterange(period)
        try:
            total_cents = self.receipt_repo.get_total_spending(
                user_id, start_date=start, end_date=end
            )

            # place is some table or smth. create

            logger.info(
                f"Successfully calculated user {user_id} expenses for period {period}"
            )
            return True

        except Exception as e:
            logger.error(
                f"Failed to calculate period {period} expenses for user {user_id}."
                f"Exception: {e}"
            )
            return False
