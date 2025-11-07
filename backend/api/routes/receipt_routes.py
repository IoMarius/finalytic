from fastapi import (
    APIRouter,
    File,
    UploadFile,
    Form,
    HTTPException,
    BackgroundTasks,
)
from models.receipt import APIResponse
from services.receipt_service import process_raw_receipt

# from core.pipeline import process_receipt


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

    background_tasks.add_task(process_raw_receipt, receipt, uid)

    return APIResponse(
        success=True,
        message="🔎 Analyzing your receipt...",
    )
