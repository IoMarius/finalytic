from datetime import date, timedelta
from data import CalculationPeriod


def period_to_daterange(
    period: CalculationPeriod, reference: date | None = None
) -> tuple[date, date]:
    reference = reference or date.today()

    if period == CalculationPeriod.WEEK:        
        start = reference - timedelta(days=reference.weekday())
        end = start + timedelta(days=6)

    elif period == CalculationPeriod.MONTH:
        start = reference.replace(day=1)
        if reference.month == 12:
            end = reference.replace(
                year=reference.year + 1, month=1, day=1
            ) - timedelta(days=1)
        else:
            end = reference.replace(month=reference.month + 1, day=1) - timedelta(
                days=1
            )

    elif period == CalculationPeriod.YEAR:
        start = reference.replace(month=1, day=1)
        end = reference.replace(month=12, day=31)

    else:
        raise ValueError(f"Unknown period: {period}")

    return start, end