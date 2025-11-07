import os
from core.commands import start_command, handle_image_command
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
from data.database import init_db

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")


init_db()

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start_command))
app.add_handler(MessageHandler(filters.PHOTO, handle_image_command))

app.run_polling()
