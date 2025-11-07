# import os
# import traceback
# from dotenv import load_dotenv
# from models.receipt import ReceiptSummary
# from pydantic import ValidationError
# from .logger import logger
# from .ocr import extract_receipt_info
# from .llm_parser import convert_to_model
# from .telegram_bot import TelegramBot

# load_dotenv()
# BOT = TelegramBot(bot_token=os.getenv("BOT_TOKEN"))
# OCR_BLOCKS_THRESHOLD = int(os.getenv("OCR_BLOCKS_THRESHOLD"))


# def process_receipt(image_bytes: bytes, uid: str):
#     logger.info(f"Processing receipt from user {uid}")

#     try:
#         receipt_text, total_blocks = extract_receipt_info(image_bytes)
#         if (
#             total_blocks < OCR_BLOCKS_THRESHOLD
#             or not receipt_text
#             or not receipt_text.strip()
#         ):
#             logger.warning(
#                 f"Could not extract text from receipt image.\nBlocks: {total_blocks}.\n Text:{receipt_text}"
#             )
#             raise ValueError(
#                 "Could not extract text from receipt image.",
#             )

#         receipt = convert_to_model(receipt_text)

#         summary = ReceiptSummary(
#             merchant_name=receipt.merchant_name,
#             currency=receipt.currency,
#             total_amount=receipt.total_amount,
#             total_items=len(receipt.line_items),
#         )

#         BOT.send_receipt_summary(uid, summary)
#     except ValidationError as e:
#         logger.error("Pipeline ocr to json validation exception.", e)

#         error_messages = []
#         for err in e.errors():
#             location = " → ".join(str(l) for l in err["loc"])
#             message = err["msg"]
#             error_messages.append(f"{location}: {message}")

#         formatted_errors = "\n".join(error_messages)

#         BOT.send_message(
#             chat_id=uid,
#             text=f"💥 <b>Something unexpected happened!</b>\n📝 Details:\n{formatted_errors}",
#         )
#     except Exception as e:
#         traceback.print_exc()
#         logger.error(f"Pipeline ocr to json exception.", e)

#         BOT.send_message(
#             chat_id=uid,
#             text=f"💥 <b>Something unexpected happened!</b>\n📝 Details: {e}",
#         )
