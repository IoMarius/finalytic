from jobs import scheduler, UsersExpensesJob
from data.repositories import UserRepository, ReceiptRepository
from data import CalculationPeriod

from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger


if not scheduler.get_job("user-expenses-by_year"):
    job = UsersExpensesJob(UserRepository, ReceiptRepository)
    scheduler.add_job(
        job.for_all_users(CalculationPeriod.YEAR),
        trigger=CronTrigger(month=12, day=31, hour=23, minute=59),
        id="user-expenses-years",
        replace_existing=True,
    )

# if not scheduler.get_job("ten_minute_job"):
#     scheduler.add_job(
#         periodic_task,
#         trigger=IntervalTrigger(minutes=10),
#         id="ten_minute_job",
#         replace_existing=True,
#     )


# scheduler.add_job(
#     my_job,
#     trigger=CronTrigger(day=1, hour=0, minute=0),
#     id="monthly_job",
#     replace_existing=True
# )
