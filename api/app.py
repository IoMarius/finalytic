import os
from dotenv import load_dotenv
from fastapi import (
    FastAPI,
    APIRouter,
    File,
    UploadFile,
    Form,
    HTTPException,
    BackgroundTasks,
)
from models.receipt import APIResponse
from core.pipeline import process_receipt


load_dotenv()
API_HOST = os.getenv("API_HOST", "127.0.0.1")
API_PORT = int(os.getenv("API_PORT", 8085))

app = FastAPI(title="Finalytic API")
receipt_router = APIRouter(prefix="/api/v1/receipts")


@receipt_router.post("")
async def store_as_json(
    background_tasks: BackgroundTasks,
    photo: UploadFile = File(...),
    uid: str = Form(...),
) -> APIResponse:
    if photo.content_type not in ["image/jpeg", "image/jpg", "image/png"]:
        raise HTTPException(
            status_code=400, detail="Only JPG or PNG images are allowed"
        )

    receipt = await photo.read()

    background_tasks.add_task(process_receipt, receipt, uid)

    return APIResponse(
        success=True,
        message="🔎 Analyzing your receipt...",
    )


app.include_router(receipt_router)

if __name__ == "__main__":
    import uvicorn
    from data.database import init_db

    init_db()
    uvicorn.run("app:app", host=API_HOST, port=API_PORT, reload=True)
