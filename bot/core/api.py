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


# async def upload_receipt(
#     uid: str,
#     filename: str,
#     image_data: bytes,
#     on_success: Callable[[ReceiptSummary], None],
#     on_retry: Callable[[int, float], None],
#     on_fail: Callable[[int, str | None], None],
#     retries: int = 3,
# ) -> bool:
#     """Send the file to the external API with retries and exponential backoff."""
#     delay = 3

#     async with httpx.AsyncClient(timeout=10.0) as client:
#         for attempt in range(1, retries + 1):
#             try:
#                 files = {"photo": (filename, image_data, "image/jpg")}
#                 data = {"uid": uid}

#                 response = await client.post(API_URL, data=data, files=files)

#                 if response.status_code == 200:
#                     logger.info(
#                         f"Successfully sent {filename}, response: {response.text}"
#                     )
#                     api_response = APIResponse[ReceiptSummary](**response.json())

#                     if api_response.success and api_response.data:
#                         await on_success(api_response.data)
#                         return True
#                     else:
#                         await on_fail(0, api_response.message)
#                         return False
#                 else:
#                     logger.warning(
#                         f"Attempt {attempt}: server returned {response.status_code}, response: {response.text}"
#                     )
#                     # Stop retrying on server errors
#                     await on_fail(attempt, f"HTTP {response.status_code}")
#                     return False

#             except httpx.RequestError as e:
#                 logger.warning(f"Attempt {attempt}: network error: {e}")

#             # Retry network failures only
#             if attempt < retries:
#                 jitter = random.uniform(0.5, 1.5)
#                 sleep_time = delay**attempt * jitter
#                 await on_retry(attempt + 1, sleep_time)
#                 logger.info(f"Retrying in {sleep_time:.1f}s (attempt {attempt + 1})")
#                 await asyncio.sleep(sleep_time)

#     # Max retries reached
#     await on_fail(retries, "Max retries reached")
#     logger.error(f"Giving up on {filename} for user {uid} after {retries} attempts")
#     return False


# async def upload_receipt(
#     uid: str,
#     filename: str,
#     image_data: bytes,
#     on_success: Callable[[ReceiptSummary], None],
#     on_retry: Callable[[int, float], None],
#     on_fail: Callable[[int, str | None], None],
#     retries=3,
# ) -> bool:
#     """Send the file to the external API with retries and exponential backoff."""
#     delay = 3
#     for attempt in range(1, retries + 1):
#         try:

#             files = {"photo": (filename, image_data, "image/jpg")}
#             data = {"uid": uid}

#             response = requests.post(API_URL, data=data, files=files)

#             if response.ok:
#                 logger.info(
#                     f"Successfully sent {filename} to API, response: {response.text}"
#                 )
#                 api_response = APIResponse[ReceiptSummary](**response.json())

#                 if api_response.success and api_response.data:
#                     await on_success(api_response.data)
#                     return True
#                 else:
#                     await on_fail(0, api_response.message)
#                     return False
#             else:
#                 logger.info(
#                     f"Attempt {attempt}: Failed to send {filename} of user {uid} to API, "
#                     f"status: {response.status_code}, response: {response.text}"
#                 )
#         except Exception as e:
#             logger.info(
#                 f"Attempt {attempt}: Error sending {filename} of  user {uid} to API: {e}"
#             )

#         if attempt < retries:
#             jitter = random.uniform(0.5, 1.5)
#             sleep_time = delay**attempt * jitter
#             await on_retry(attempt + 1, sleep_time)

#             logger.info(f"Retrying in {sleep_time:.1f}s (attempt {attempt + 1})")
#             await asyncio.sleep(sleep_time)

#     await on_fail(retries)
#     logger.info(f"Giving up on {filename} of user {uid} after {retries} attempts")
#     return False
