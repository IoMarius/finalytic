import os
import traceback

from services import (
    ValidationError,
    logger,
    load_dotenv,
    extract_receipt_info,
    convert_receipt_text_to_json,
    TelegramBot,
    get_session,
    UserRepository,
    ReceiptRepository,
    ReceiptMapper,
    ImageManager,
    Receipt,
    ReceiptSummary,
)


load_dotenv()
BOT = TelegramBot(bot_token=os.getenv("BOT_TOKEN"))
OCR_BLOCKS_THRESHOLD = int(os.getenv("OCR_BLOCKS_THRESHOLD"))


async def process_raw_receipt(image_bytes: bytes, telegram_uid: str):
    try:
        user_id = await _create_user_if_missing(telegram_uid)
        logger.info(f"Processing receipt from user {user_id}")

        receipt_text, total_blocks = extract_receipt_info(image_bytes)
        if (
            total_blocks < OCR_BLOCKS_THRESHOLD
            or not receipt_text
            or not receipt_text.strip()
        ):
            logger.warning(
                f"Could not extract text from receipt image.\nBlocks: {total_blocks}.\n Text:{receipt_text}"
            )
            raise ValueError(
                "Could not extract text from receipt image.",
            )

        receipt = convert_receipt_text_to_json(receipt_text)
        await _store_receipt(receipt, image_bytes, user_id)

        summary = ReceiptSummary(
            merchant_name=receipt.merchant_name,
            currency=receipt.currency,
            total_amount=receipt.total_amount,
            total_items=len(receipt.line_items),
        )

        BOT.send_receipt_summary(telegram_uid, summary)
    except ValidationError as e:
        logger.error("Pipeline ocr to json validation exception.", e)

        error_messages = []
        for err in e.errors():
            location = " → ".join(str(l) for l in err["loc"])
            message = err["msg"]
            error_messages.append(f"{location}: {message}")

        formatted_errors = "\n".join(error_messages)

        BOT.send_message(
            chat_id=telegram_uid,
            text=f"💥 <b>Something unexpected happened!</b>\n📝 Details:\n{formatted_errors}",
        )
    except Exception as e:
        traceback.print_exc()
        logger.error(f"Pipeline ocr to json exception.", e)

        BOT.send_message(
            chat_id=telegram_uid,
            text=f"💥 <b>Something unexpected happened!</b>\n📝 Details: {e}",
        )


async def _create_user_if_missing(telegram_uid: str) -> str:  # user id (internal)
    async with get_session() as session:
        repo = UserRepository(session)
        userExists = await repo.user_exists(telegram_id=telegram_uid)

        if userExists:
            user = await repo.get_by_telegram_id(telegram_uid)
            return user.id

        new_user = await repo.create_user(telegram_uid, None)  # no passphrase for nowF
        return new_user.id


async def _store_receipt(receipt: Receipt, image_bytes: bytes, user_id: str):
    images = ImageManager()
    store_result = images.save_receipt_image(image_bytes, user_id)

    mapper = ReceiptMapper()
    db_receipt = mapper.convert_complete_receipt(receipt, user_id)
    db_receipt.receipt_lq_image_path = store_result["relative_path"]

    async with get_session() as session:
        repo = ReceiptRepository(session)
        await repo.create(db_receipt)
        logger.debug(f"Receipt saved successfully for user {user_id}")
