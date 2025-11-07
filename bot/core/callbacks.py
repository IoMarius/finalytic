import os
from telegram import Update
from data import database as db
from .logger import logger


class ReceiptCallbacks:
    """Factory for creating receipt upload callbacks with side effects"""

    @staticmethod
    def create_success_handler(
        update: Update, receipt_id: str, uid: str, filepath: str
    ):
        from data.database import ReceiptUploadStatus

        async def on_success(response: str):
            success = db.set_receipt_status(
                receipt_id=receipt_id, uid=uid, status=ReceiptUploadStatus.UPLOADED
            )
            if success:
                logger.info(f"Receipt {receipt_id} marked as COMPLETED")

            try:
                os.remove(filepath)
                logger.info(f"Deleted local file {filepath}")
            except Exception as e:
                logger.error(f"Failed to delete {filepath}: {e}")

            await update.message.reply_text(response, parse_mode="Markdown")

        return on_success

    @staticmethod
    def create_fail_handler(update: Update, receipt_id: str, uid: str):
        from data.db_models import ReceiptUploadStatus

        async def on_fail(failure_reason: str):
            db.set_receipt_status(
                receipt_id=receipt_id, uid=uid, status=ReceiptUploadStatus.FAILED
            )
            logger.info(f"Receipt {receipt_id} marked as FAILED to upload.")

            await update.message.reply_text(
                f"{failure_reason}\nPlease try again later."
            )

        return on_fail
