def main():
    from core.commands import start_command, handle_image_command
    from data.database import init_db
    from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
    from core.logger import logger
    import os
    from dotenv import load_dotenv

    load_dotenv()
    TOKEN = os.getenv("BOT_TOKEN")

    init_db()

    logger.info("Configuring bot")
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(MessageHandler(filters.PHOTO, handle_image_command))

    logger.info("Bot running.")
    app.run_polling()


if __name__ == "__main__":
    main()
