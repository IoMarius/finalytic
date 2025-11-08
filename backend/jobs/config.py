
from job_scheduler import scheduler, CronTrigger


# scheduler.add_job()
# if not scheduler.get_job("ten_minute_job"):
#     scheduler.add_job(
#         periodic_task,
#         trigger=IntervalTrigger(minutes=10),
#         id="ten_minute_job",
#         replace_existing=True,
#     )
