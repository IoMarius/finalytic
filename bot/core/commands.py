import os
import asyncio
from .file_handler import FileHandler
from .callbacks import ReceiptCallbacks
from .logger import logger
from .api import upload_receipt
from telegram import Update
from dotenv import load_dotenv
from data import database as db

load_dotenv()
DATA_DIR = "data/files"
RECEIPTS_DIR = os.path.join(DATA_DIR, "receipts")

os.makedirs(RECEIPTS_DIR, exist_ok=True)


async def start_command(update: Update, _):
    await update.message.reply_text("Hello! Send me the receipts.")
    logger.info(f"User {update.effective_user.id} started the bot.")


async def handle_image_command(update: Update, _):
    if not update.message.photo:
        return

    uid = update.effective_user.id
    photo = update.message.photo[-1]
    
    file_handler = FileHandler(DATA_DIR)
    user_dir = file_handler.get_user_directory(uid)
    filename = file_handler.generate_filename()
    filepath = os.path.join(user_dir, filename)

    image_data = await file_handler.download_photo(photo, filepath)
    logger.info(f"Saved image for user {uid} to {filepath}.")

    receipt_id = db.add_receipt(filepath=filepath, uid=str(uid), filename=filename)

    logger.info(f"Created receipt {receipt_id} with status PENDING")

    on_success = ReceiptCallbacks.create_success_handler(
        update=update, receipt_id=receipt_id, uid=str(uid), filepath=filepath
    )

    on_fail = ReceiptCallbacks.create_fail_handler(
        update=update, receipt_id=receipt_id, uid=str(uid)
    )

    asyncio.create_task(
        upload_receipt(
            uid=str(uid),
            filename=filename,
            image_data=image_data,
            on_success=on_success,        
            on_fail=on_fail,
        )
    )    
