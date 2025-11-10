import os
from jobs import load_dotenv, SQLAlchemyJobStore, AsyncIOScheduler

load_dotenv()
DATABASE_URL = (
    f"postgresql+psycopg2://"
    f"{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
    f"@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}"
    f"/{os.getenv('POSTGRES_DB')}"
)

jobstores = {
    "default": SQLAlchemyJobStore(
        url=DATABASE_URL,
        tablename="apscheduler_jobs",
        engine_options={"connect_args": {"options": "-csearch_path=scheduled"}},
    )
}

scheduler = AsyncIOScheduler(jobstores)
