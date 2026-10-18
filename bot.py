import os
import threading
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")

# Fake web server so Render Free tier go keep am alive
app_web = Flask(__name__)
@app_web.route('/')
def home():
    return "THE7THONE BOT IS LIVE 24/7!"

def run_web():
    app_web.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🔥 THE7THONE BOT ONLINE 24/7! Send any link.")

async def handle_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"You said: {update.message.text}")

def run_bot():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_msg))
    print("Bot running...")
    app.run_polling()

if __name__ == "__main__":
    threading.Thread(target=run_web).start()
    run_bot()
