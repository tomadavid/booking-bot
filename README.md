# 🤖 Booking Bot — Gemini × Telegram × Google Calendar Integration

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Google Calendar API](https://img.shields.io/badge/API-Google%20Calendar-red.svg)
![Telegram Bot](https://img.shields.io/badge/Telegram-Bot-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

A **Telegram chatbot** that automates scheduling and booking using **Google Calendar**.  
It ensures events don’t overlap on the host’s calendar and automatically creates calendar entries for both host and client.

---

## ✨ Features
- 🗓️ Google Calendar integration with OAuth2 authentication  
- 🤖 Natural chat-based booking with Gemini through Telegram  
- ✅ Prevents overlapping host events  
- 📧 Creates events for both host and client  
- 🌍 Time zone–aware scheduling  
- 🔒 Secure token management for each user  

---

## 📂 Project Structure

```
booking-bot/
│
├── google_calendar.py     # Handles low level Google Calendar logic (create/check events)
├── orchestrator.py        # Main orchestration logic (LLM processes client's request)
├── telegram_bot.py        # Telegram bot entry point
├── parser.py              # LLM's output parser (limits LLM for program's fuctionality)
├── modules.py             # Basic program's modules (schedule/cancel/reschedule)
├── requirements.txt       # Python dependencies
│
├── credentials.json       # Google OAuth credentials (DO NOT COMMIT)
├── token_host.json        # Host's OAuth token (auto-generated)
├── token_client.json      # Client's OAuth token (auto-generated)
│
└── .env                   # Telegram bot token, LLM API keys and environment settings
```

---

## Demo
<img width="1080" height="1558" alt="image" src="https://github.com/user-attachments/assets/ec22c17f-8bfa-45c5-b8b8-829a513bb5a9" />

## ⚙️ Setup

### 1️⃣ Clone the repository
```bash
git clone https://github.com/tomadavid/booking-bot.git
cd booking-bot
```

### 2️⃣ Create a virtual environment
```bash
python -m venv .env
source .env/bin/activate      # macOS/Linux
.env\Scripts\activate         # Windows
```

### 3️⃣ Install dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Add required files

#### 🧩 `credentials.json`
- Go to [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
- Create an **OAuth 2.0 Client ID** (type: Desktop App)
- Download and rename the file to `credentials.json`
- Place it in the project root

Used to generate:
- `token_host.json` (for the host account)
- `token_client.json` (for each client authorization)

#### 🔐 `.env`
Replace environment variables on `.env` file with your variables:
```
GEMINI_API_KEY=your_gemini_API_key_here
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
```

---

## 🚀 Running the Bot
```bash
python telegram_bot.py
```

On the first run:
- You’ll be prompted to log in with the **host’s Google account** (creates `token_host.json`)
(In production, `token_host.json` is already in the environment. Only `token_client.json` must be created for the client that logs)
- When a **client** interacts with the bot, they’ll be prompted for OAuth (creates `token_client.json`)

The bot will then check the host’s calendar for conflicts and automatically create events on both calendars.

---

## 🔒 Security Notes
Do **not** upload or commit the following files:
```
.env
credentials.json
token_*.json
```

Add them to `.gitignore`:
```
# Sensitive files
.env
credentials.json
token_host.json
token_client.json
```

---

## 🧠 Future Improvements
- 🔁 Add booking rescheduling/cancellation  
- 📊 Admin dashboard  

---

## 👤 Author
Developed by **David Toma**  
Building intelligent systems that integrate AI and automation.
