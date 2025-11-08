# Finalytic - Self-Hosted Receipt Tracking Bot

A self-hosted Telegram bot for tracking expenses by analyzing receipt photos and QR codes. Built with FastAPI and Python Telegram Bot.

---

## 🌟 Features

### Receipt Processing
- 📸 Upload receipts via photo
- 🔍 QR code scanning support
- 🤖 AI-powered text extraction and parsing
- 🧾 Automatic merchant, items and total detection

### Analysis
- 📊 Spending categorization
- 💰 Track expenses by merchant
- 📅 Filter by date ranges
- 🔄 Currency support
- more to come...

### Data Management
- 💾 Stores full receipt details including:
  - Merchant information
  - Individual item prices and quantity
  - Total amount and currency
  - Payment method
  - Additional metadata (tax ID, cashier, store address, etc)



---

## 🛠️ Architecture

The application consists of two individual main components:

1. **Telegram Bot** - Handles user interaction and receipt photo uploads  
2. **Backend API** - Processes receipts using OCR and AI analysis

---

## Tech Stack
- Python 3.13+
- FastAPI
- SQLModel/SQLAlchemy
- OpenAI GPT
- PaddleOCR
- PostgreSQL
- SQLite (for bot storage)

---

## 🚀 Getting Started

### Prerequisites
- Python 3.13+
- Telegram Bot Token
- OpenAI API Key
- PostgreSQL database

### Installation
1. Clone the repository
2. Set up environment variables for bot:
3. Set up environment variables for backend:
4. Install dependencies and run:

Or using Docker:
- comming soon...
---

## 📝 Usage
1. Start a chat with your bot on Telegram  
2. Send `/start` to initialize  
3. Send receipt photos or share QR codes  
4. The bot will process and store the receipt information
... more to come

---

## 📜 License
This project is licensed under a **Custom MIT Non-Commercial License**. For personal or educational use only. See the LICENSE file for details.

---

## 🤝 Contributing
Contributions welcome!

---
