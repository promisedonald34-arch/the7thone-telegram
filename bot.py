import os
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from flask import Flask
import threading

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "7738226053"))

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@app.route('/')
def home(): return "THE7THONE ORDER BOT LIVE!"

def run_flask():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

user_orders = {}

def main_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row(KeyboardButton("TOPS 🔥"), KeyboardButton("BOTTOMS"))
    markup.row(KeyboardButton("FOOTWEAR 👟"), KeyboardButton("🛒 PLACE ORDER"))
    markup.row(KeyboardButton("💳 PAYMENT"))
    return markup

@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id, 
        "Welcome to *THE 7TH ONE* 🖤\n\nSelect what you need below 👇\n\n👕 TOPS - Gucci, Balenciaga\n👖 BOTTOMS - Cargo, Jeans\n👟 FOOTWEAR - Sneakers, Slides\n\nClick PLACE ORDER to order",
        reply_markup=main_keyboard(), parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.text == "TOPS 🔥")
def tops(m):
    bot.send_message(m.chat.id, "🔥 *TOPS AVAILABLE*\n\n• Gucci Tee - 15k (M/L/XL)\n• Balenciaga - 22k\n• Vintage Tee - 10k\n\nSend as: `Gucci | M | Your Address | Phone`", parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.text == "BOTTOMS")
def bottoms(m):
    bot.send_message(m.chat.id, "👖 *BOTTOMS*\n\n• Cargo - 18k\n• Jean - 16k\n• Shorts - 8k\n\nSend as: `Cargo | L | Your Address | Phone`", parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.text == "FOOTWEAR 👟")
def footwear(m):
    bot.send_message(m.chat.id, "👟 *FOOTWEAR*\n\n• Sneakers - 25k+\n• Slides - 12k\n\nSend as: `Sneakers | 43 | Your Address | Phone`", parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.text == "🛒 PLACE ORDER")
def place_order(m):
    bot.send_message(m.chat.id, "📦 *To Place Order, send in this format:*\n\n`Product | Size | Address | Phone`\n\nExample:\n`Gucci | M | Allen Ave Ikeja | 09048365677`\n\nJust type it now!", parse_mode="Markdown")
    user_orders[m.chat.id] = "waiting"

@bot.message_handler(func=lambda m: m.text == "💳 PAYMENT")
def payment(m):
    bot.send_message(m.chat.id, 
        "💳 *PAYMENT DETAILS*\n\n"
        "Bank: *OPay*\n"
        "Acct No: `7045816469`\n"
        "Name: *Promise Emeka*\n\n"
        "After payment, send screenshot proof here. We confirm ASAP! 🙏\n\n"
        "Tap and hold number to copy",
        parse_mode="Markdown")

@bot.message_handler(func=lambda m: "|" in m.text and len(m.text.split("|")) >= 3)
def capture_order(m):
    try:
        parts = [p.strip() for p in m.text.split("|")]
        product = parts[0]
        size = parts[1] if len(parts) > 1 else "N/A"
        address = parts[2] if len(parts) > 2 else "N/A"
        phone = parts[3] if len(parts) > 3 else "N/A"
        
        bot.send_message(m.chat.id, 
            f"✅ *Order Received!*\n\nProduct: {product}\nSize: {size}\nAddress: {address}\nPhone: {phone}\n\nPlease click 💳 PAYMENT to pay.\n\nAcc No: `7045816469` (OPay - Promise Emeka)",
            parse_mode="Markdown")
        
        admin_msg = f"📦 *NEW ORDER (No proof yet)*\nFrom: {m.chat.id} {f'@{m.from_user.username}' if m.from_user.username else 'No username'}\nProduct: {product} | Size: {size}\nAddress: {address}\nPhone: {phone}"
        bot.send_message(ADMIN_ID, admin_msg, parse_mode="Markdown")
        user_orders[m.chat.id] = f"{product} | {size} | {address}"
    except:
        bot.send_message(m.chat.id, "Format error. Use: Product | Size | Address | Phone")

@bot.message_handler(content_types=['photo'])
def payment_proof(m):
    bot.send_message(m.chat.id, "✅ *PAYMENT PROOF RECEIVED!* We will confirm and ship your order shortly. Thanks for trusting THE7THONE 🖤", parse_mode="Markdown")
    try:
        bot.forward_message(ADMIN_ID, m.chat.id, m.message_id)
        caption = f"💸 *PAYMENT PROOF RECEIVED*\nFrom: {m.chat.id} {f'@{m.from_user.username}' if m.from_user.username else 'No username'}\nOrder: {user_orders.get(m.chat.id, 'See previous')}\nTime: Proof just sent"
        bot.send_message(ADMIN_ID, caption, parse_mode="Markdown")
    except:
        pass

@bot.message_handler(func=lambda m: True)
def fallback(m):
    bot.send_message(m.chat.id, "Use buttons below 👇 or send order as:\n`Product | Size | Address | Phone`", reply_markup=main_keyboard(), parse_mode="Markdown")

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    bot.infinity_polling()
