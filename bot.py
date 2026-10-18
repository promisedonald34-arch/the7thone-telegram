import os
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask
import threading
import time

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 7738226053

bot = telebot.TeleBot(BOT_TOKEN, threaded=False)
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
    bot.send_message(m.chat.id, "Welcome to *THE 7TH ONE* 🖤\n\nClick 🛒 PLACE ORDER to order\nClick 💳 PAYMENT to see account\n\nBank: OPay 7045816469 Promise Emeka", reply_markup=main_keyboard(), parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.text == "🛒 PLACE ORDER")
def place_order(m):
    bot.send_message(m.chat.id, "📦 Send: `Product | Size | Address | Phone`\nExample: `Gucci | M | Allen Ave | 09048365677`", parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.text == "💳 PAYMENT")
def payment(m):
    bot.send_message(m.chat.id, "💳 *PAYMENT DETAILS*\n\nBank: *OPay*\nAcct No: `7045816469`\nName: *Promise Emeka*\n\nAfter payment, send screenshot here.", parse_mode="Markdown")

@bot.message_handler(func=lambda m: "|" in m.text and len(m.text.split("|")) >= 3)
def capture_order(m):
    parts = [p.strip() for p in m.text.split("|")]
    product, size, address, phone = parts[0], parts[1], parts[2], parts[3] if len(parts)>3 else "N/A"
    bot.send_message(m.chat.id, f"✅ Order saved! {product} | {size}\nNow pay to 7045816469 and send proof", parse_mode="Markdown")
    try:
        bot.send_message(ADMIN_ID, f"📦 *NEW ORDER*\nFrom: {m.chat.id} @{m.from_user.username or ''}\nProduct: {product} | Size: {size}\nAddr: {address}\nPhone: {phone}", parse_mode="Markdown")
    except: pass
    user_orders[m.chat.id] = f"{product} | {size}"

@bot.message_handler(content_types=['photo'])
def payment_proof(m):
    customer_id = m.chat.id
    bot.send_message(customer_id, "⏳ *PROOF RECEIVED!* Verifying payment to OPay 7045816469...", parse_mode="Markdown")
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton("✅ APPROVE", callback_data=f"approve_{customer_id}"),
        InlineKeyboardButton("❌ REJECT", callback_data=f"reject_{customer_id}")
    )
    try:
        bot.send_photo(ADMIN_ID, m.photo[-1].file_id, 
            caption=f"💸 *PAYMENT PROOF*\nFrom: {customer_id} @{m.from_user.username or ''}\nOrder: {user_orders.get(customer_id,'')}\n\nOPay 7045816469 - Received?",
            parse_mode="Markdown", reply_markup=markup)
    except Exception as e:
        print(f"Admin send failed: {e}")

@bot.callback_query_handler(func=lambda call: True)
def handle_approve_reject(call):
    if call.from_user.id != ADMIN_ID: return
    action, cid = call.data.split("_")
    cid = int(cid)
    if action == "approve":
        bot.send_message(cid, "✅ *PAYMENT CONFIRMED!* Received to OPay 7045816469 Promise Emeka. Your order is shipping! 🖤")
        bot.edit_message_caption(f"✅ APPROVED for {cid}", call.message.chat.id, call.message.message_id)
    else:
        bot.send_message(cid, "❌ *NOT RECEIVED* We checked OPay 7045816469 Promise Emeka - not seen. Check number and resend proof with ID.")
        bot.edit_message_caption(f"❌ REJECTED for {cid}", call.message.chat.id, call.message.message_id)
    bot.answer_callback_query(call.id, f"{action}d")

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    # FIX for 409 Conflict
    try:
        bot.remove_webhook()
        time.sleep(1)
    except: pass
    bot.infinity_polling(skip_pending=True, timeout=30, long_polling_timeout=30)
