import requests
from models.receipt import ReceiptSummary

class TelegramBot:
    def __init__(self, bot_token: str):
        self.bot_token = bot_token
        self.api_url = f"https://api.telegram.org/bot{bot_token}"

    def send_message(self, chat_id: str | int, text: str) -> dict:
        """
        Sends a message to a user or chat.

        :param chat_id: Telegram chat ID or user ID
        :param text: Message text
        :return: Response from Telegram API as dict
        """
        url = f"{self.api_url}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": text,
            "parse_mode": "HTML",  # optional, supports HTML/Markdown formatting
        }

        try:
            response = requests.post(url, json=payload, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"[ERROR] Failed to send message: {e}")
            return {"ok": False, "error": str(e)}

    def send_receipt_summary(self, chat_id: str | int, summary: ReceiptSummary) -> dict:
        """
        Sends a formatted receipt summary to a user.

        :param chat_id: Telegram chat ID or user ID
        :param summary: ReceiptSummary object
        :return: Response from Telegram API as dict
        """
        message = "🧾 <b>Receipt Processed</b>\n\n"
        if summary.merchant_name:
            message += f"🏪 Merchant: <i>{summary.merchant_name}</i>\n"

        message += f"🛒 Items: <b>{summary.total_items}</b>\n"
        message += f"💰 Total: <b>{summary.total_amount} {summary.currency}</b>"


        return self.send_message(chat_id, message)
