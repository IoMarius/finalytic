from fastapi import (
    APIRouter,
    File,
    UploadFile,
    Form,
    HTTPException,
)
import asyncio
from models.receipt import APIResponse
from services.receipt_service import process_raw_receipt
from jobs import run_for_user

# from core.pipeline import process_receipt


receipt_router = APIRouter(prefix="/api/v1/receipts")


@receipt_router.post("")
async def store_as_json(
    photo: UploadFile = File(...),
    uid: str = Form(...),
) -> APIResponse:
    if photo.content_type not in ["image/jpeg", "image/jpg", "image/png"]:
        raise HTTPException(
            status_code=400, detail="Only JPG or PNG images are allowed"
        )

    receipt = await photo.read()

    async def process_and_calculate(uid: str, receipt: bytes):
        user_id = await process_raw_receipt(image_bytes=receipt, telegram_uid=uid)
        await run_for_user(user_id)

    asyncio.create_task(
        process_and_calculate(
            uid,
            receipt,
        )
    )

    return APIResponse(
        success=True,
        message="🔎 Analyzing your receipt...",
    )
