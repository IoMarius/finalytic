import os
from dotenv import load_dotenv
from fastapi import FastAPI
from api.routes.receipt_routes import receipt_router
from api.routes.user_routes import user_router

load_dotenv()
API_HOST = os.getenv("API_HOST", "127.0.0.1")
API_PORT = int(os.getenv("API_PORT", 8085))

app = FastAPI(title="Finalytic API")

app.include_router(receipt_router)
app.include_router(user_router)

if __name__ == "__main__":
    import uvicorn
    from data.database import init_db

    init_db()
    uvicorn.run("app:app", host=API_HOST, port=API_PORT, reload=True)
