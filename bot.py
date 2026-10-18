import os
import threading
from flask import Flask
import telebot

TOKEN = os.getenv("BOT_TOKEN")
print(f"TOKEN EXISTS: {TOKEN is not None}")

bot = telebot.TeleBot(TOKEN)
web = Flask(__name__)

@web.route('/')
def home():
    return "THE7THONE LIVE 24/7!"

def run_web():
    web.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))

@bot.message_handler(commands=['start'])
def start(m):
    bot.reply_to(m, "🔥 THE7THONE BOT ONLINE 24/7! Send Terabox link")

@bot.message_handler(func=lambda m: True)
def handle(m):
    bot.reply_to(m, f"Got: {m.text}")

def run_bot():
    print("Bot running... START")
    bot.infinity_polling()

if __name__ == "__main__":
    threading.Thread(target=run_web, daemon=True).start()
    run_bot()
