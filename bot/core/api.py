import os
import random

# import requests
import httpx
import asyncio
from .logger import logger
from dotenv import load_dotenv
from typing import Callable
from models.receipt import APIResponse

load_dotenv()
API_URL = os.getenv("API_URL", "https://example.com/api/upload")


async def upload_receipt(
    uid: str,
    filename: str,
    image_data: bytes,
    on_success: Callable[[str], None],
    on_fail: Callable[[str], None],
) -> None:
    """
    Send the file to the external API.

    :param uid: User ID
    :param filename: Name of the image file
    :param image_data: Image bytes
    :param on_success: Called with ReceiptSummary if upload succeeds
    :param on_fail: Called with error message if upload fails
    """
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            files = {"photo": (filename, image_data, "image/jpg")}
            data = {"uid": uid}

            response = await client.post(API_URL, data=data, files=files)
            response.raise_for_status()  # raises if status != 200

            api_response = APIResponse(**response.json())
            if api_response.success:
                await on_success(api_response.message)
            else:
                await on_fail(api_response.message or "Unknown error from API")

    except httpx.RequestError as e:
        await on_fail(f"🤖 Network error: {e}")
    except Exception as e:
        await on_fail(f"🤖 Exception:{str(e)}")
