import datetime
from langdetect import detect
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

BOT_TOKEN = '7691378301:AAEKM96-3_r7GF1GEP2aB_AQKav74xYIRWs'
WARNING_MESSAGE = "⚠️ Повідомлення видалене. На вихідних заборонені повідомлення мовою росії."

def is_weekend():
    return datetime.datetime.today().weekday() >= 5  # 5 = Saturday or Sunday

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    text = update.message.text
    sender = update.message.from_user.username or update.message.from_user.first_name
    chat_id = update.message.chat_id

    if not text:
        return

    print(f"📩 Message from {sender} in chat {chat_id}: {text}")

    if is_weekend():
        try:
            language = detect(text)
            print(f"🌐 Detected language: {language}")

            if language == 'ru':
                print(f"🛑 Deleting message from {sender} (Russian on weekend)")
                await update.message.delete()
                await update.message.chat.send_message(WARNING_MESSAGE)
            else:
                print(f"✅ Message from {sender} allowed (language: {language})")
        except Exception as e:
            print(f"❌ Language detection failed: {e}")

if __name__ == '__main__':
    print("✅ Bot is starting...")
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.run_polling()
