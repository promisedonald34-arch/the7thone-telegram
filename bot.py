import os
import telebot
from flask import Flask
import threading

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "THE7THONE BOT LIVE!"

def run_flask():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

# === YOUR STORE REPLIES ===
MENU_TEXT = """🔥 *THE 7TH ONES - OFFICIAL DRIP MENU* 🔥

*👕 TOPS*
┣ Gucci Tee - 15k
┣ Balenciaga - 22k
┗ Vintage - 10k

*👖 BOTTOMS*
┣ Cargo - 18k
┣ Jean - 16k
┗ Shorts - 8k

*👟 FOOTWEAR*
┣ Sneakers - 25k+
┗ Slides - 12k

━━━━━━━━━━━━━━━━━━
💳 *PAYMENT*: Transfer / Cash on Delivery
🚚 *DELIVERY*: Lagos same day, Outside 2-3 days

Type PRICE to order 👇"""

PRICE_TEXT = """💸 *THE 7TH ONES - PRICE LIST* 💸

Why we different? Quality no be joke! 💯

🔥 *STARTER PACK - 35k*
   (Tee + Cargo + Cap)

👑 *BOSS PACK - 60k*
   (Full drip + Sneakers)

⚡ *SINGLE ITEMS - 8k to 25k*

Want discount? Type OWNER and say "7TH GANG" for 10% OFF! 😉"""

LOCATION_TEXT = """📍 *WE ARE IN LAGOS!*

🏠 Main: Yaba, Lagos
🚚 Delivery to:
    - Lagos - 2k-4k (Today)
    - Ibadan - 3k
    - Abuja - 5k
    - Everywhere else - We ship!

Type OWNER to drop your location 📦"""

OWNER_TEXT = """👑 *CONNECT TO THE BOSS*

The 7th One himself dey online!

📞 WhatsApp: wa.me/234YOURNUMBER
📸 IG: @the7thones
⏰ Active: 9AM - 11PM Daily

*Send your order now - We no dey dull!* 🚀"""

WELCOME = """╭━━━━━━━🔥 *THE 7TH ONE* 🔥━━━━━━━╮
┃
┃  Yo! Welcome to the wave 🌊
┃  You just tapped the realest bot in Lagos!
┃
┃  ⚡ What you wanna do?
┃  ┣ 📋 Type *MENU* - See drip
┃  ┣ 💰 Type *PRICE* - Check cost  
┃  ┣ 📍 Type *LOCATION*
┃  ┗ 👑 Type *OWNER* - Talk to boss
┃
╰━━━━━━━━━━━━━━━━━━━━━━╯"""

@bot.message_handler(commands=['start','menu','help'])
def start(m):
    bot.send_message(m.chat.id, WELCOME, parse_mode="Markdown")

@bot.message_handler(func=lambda m: True)
def reply_all(m):
    text = m.text.lower().strip() if m.text else ""
    
    if "menu" in text or "product" in text or "catalog" in text or "1" == text:
        bot.send_message(m.chat.id, MENU_TEXT, parse_mode="Markdown")
    elif "price" in text or "cost" in text or "how much" in text or "2" == text:
        bot.send_message(m.chat.id, PRICE_TEXT, parse_mode="Markdown")
    elif "location" in text or "where" in text or "deliver" in text:
        bot.send_message(m.chat.id, LOCATION_TEXT, parse_mode="Markdown")
    elif "owner" in text or "boss" in text or "order" in text or "buy" in text or "4" == text:
        bot.send_message(m.chat.id, OWNER_TEXT, parse_mode="Markdown")
    elif text in ["hi","hello","hey","yo","sup","0"]:
        bot.send_message(m.chat.id, WELCOME, parse_mode="Markdown")
    else:
        bot.send_message(m.chat.id, f"You said '{m.text}'\n\nI understand:\n*MENU* | *PRICE* | *LOCATION* | *OWNER*\n\nTry one! 👆", parse_mode="Markdown")

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    bot.infinity_polling()
