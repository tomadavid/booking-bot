from telegram.ext import Application, CommandHandler, MessageHandler, filters
from orchestrator import orchestrator
import os


"""
    Telegram Bot -> Booking system
    Client Interaction
"""

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# handle client's messages
async def handle_message(update, context):
    await update.message.reply_text(orchestrator(update.message.text))

async def start(update, context):
    await update.message.reply_text("Hello! I'm your bot.")

def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()