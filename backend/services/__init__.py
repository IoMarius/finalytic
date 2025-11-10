from models.receipt import Receipt, ReceiptSummary
from core.logger import logger
from core.ocr import extract_receipt_info
from core.llm_parser import convert_receipt_text_to_json
from core.telegram_bot import TelegramBot
from data.database import get_session
from data.repositories.user_repository import UserRepository
from data.repositories.receipt_repository import ReceiptRepository
from models.mapping.receipt_mapper import ReceiptMapper
from backend.tools.image_manager import ImageManager
from pydantic import ValidationError
from dotenv import load_dotenv
from models.calculations import CalculationPeriod
from tools.expenses_calculator import period_to_daterange