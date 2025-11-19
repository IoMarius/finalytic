from jobs import scheduler, run_for_all
from apscheduler.triggers.interval import IntervalTrigger
import asyncio


if not scheduler.get_job("all-user-expenses"):
    scheduler.add_job(
        lambda: asyncio.create_task(run_for_all()),
        trigger=IntervalTrigger(minutes=15),
        id="all-user-expenses",
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
