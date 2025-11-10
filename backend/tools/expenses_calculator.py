from tools import CalculationPeriod, date, timedelta


def period_to_daterange(
    period: CalculationPeriod, reference: date = None
) -> tuple[date, date]:
    reference = reference or date.today()
    if period == CalculationPeriod.MONTH:
        start = reference.replace(day=1)

        if reference.month == 12:
            end = reference.replace(
                year=reference.year + 1, month=1, day=1
            ) - timedelta(days=1)
        else:
            end = reference.replace(month=reference.month + 1, day=1) - timedelta(
                days=1
            )
    elif period == CalculationPeriod.QUARTER:
        quarter = (reference.month - 1) // 3 + 1
        start_month = 3 * (quarter - 1) + 1
        start = reference.replace(month=start_month, day=1)
        end_month = start_month + 2
        if end_month == 12:
            end = reference.replace(month=12, day=31)
        else:
            next_month = reference.replace(month=end_month + 1, day=1)
            end = next_month - timedelta(days=1)
    elif period == CalculationPeriod.YEAR:
        start = reference.replace(month=1, day=1)
        end = reference.replace(month=12, day=31)
    else:
        raise ValueError(f"Unknown period: {period}")

    return start, end


# class UserExpensesCalculator:
#     def __init__(self, receipt_repo: ReceiptRepository):
#         self.receipt_repo = receipt_repo

#     async def calculate_for_period(
#         self, user_id: str, period: CalculationPeriod
#     ) -> int:
#         start, end = self._get_date_range(period)
#         total_cents = await self.receipt_repo.get_total_spending(
#             user_id, start_date=start, end_date=end
#         )

#         return total_cents
