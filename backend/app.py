import os
from fastapi import FastAPI
from api.routes.receipt_routes import receipt_router
from api.routes.user_routes import user_router
from jobs.job_scheduler import scheduler
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from core.logger import logger

load_dotenv()
API_HOST = os.getenv("API_HOST", "127.0.0.1")
API_PORT = int(os.getenv("API_PORT", 8085))


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("App starting up...")
    # startup
    from data.database import init_db

    await init_db()
    scheduler.start()
    yield
    logger.info("App shutting down...")
    # shutdown
    scheduler.shutdown(wait=False)


app = FastAPI(title="Finalytic API", lifespan=lifespan)

app.include_router(receipt_router)
app.include_router(user_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host=API_HOST, port=API_PORT, reload=True)
