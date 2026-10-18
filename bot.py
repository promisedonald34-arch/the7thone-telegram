import os
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask
import threading

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = 7738226053

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
        "Welcome to *THE 7TH ONE* 🖤\n\n👕 TOPS\n👖 BOTTOMS\n👟 FOOTWEAR\n\nClick 🛒 PLACE ORDER to order\nClick 💳 PAYMENT to see account",
        reply_markup=main_keyboard(), parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.text == "🛒 PLACE ORDER")
def place_order(m):
    bot.send_message(m.chat.id, "📦 Send order as:\n\n`Product | Size | Address | Phone`\n\nExample:\n`Gucci | M | Allen Ave Ikeja | 09048365677`", parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.text == "💳 PAYMENT")
def payment(m):
    bot.send_message(m.chat.id, 
        "💳 *PAYMENT DETAILS*\n\nBank: *OPay*\nAcct No: `7045816469`\nName: *Promise Emeka*\n\nAfter payment, send screenshot here.",
        parse_mode="Markdown")

@bot.message_handler(func=lambda m: "|" in m.text and len(m.text.split("|")) >= 3)
def capture_order(m):
    parts = [p.strip() for p in m.text.split("|")]
    product, size, address, phone = parts[0], parts[1], parts[2], parts[3] if len(parts)>3 else "N/A"
    bot.send_message(m.chat.id, f"✅ Order saved!\n{product} | {size}\nNow click 💳 PAYMENT and pay to 7045816469", parse_mode="Markdown")
    bot.send_message(ADMIN_ID, f"📦 *NEW ORDER (No proof yet)*\nFrom: {m.chat.id} @{m.from_user.username or ''}\nProduct: {product} | Size: {size}\nAddress: {address}\nPhone: {phone}", parse_mode="Markdown")
    user_orders[m.chat.id] = f"{product} | {size}"

@bot.message_handler(content_types=['photo'])
def payment_proof(m):
    customer_id = m.chat.id
    customer_name = f"@{m.from_user.username}" if m.from_user.username else f"ID {customer_id}"
    order_info = user_orders.get(customer_id, "No order details yet")
    bot.send_message(customer_id, "⏳ *PAYMENT PROOF RECEIVED!* We are verifying your payment to OPay 7045816469...\n\nYou will get confirmation in a minute. 🙏", parse_mode="Markdown")
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton("✅ APPROVE", callback_data=f"approve_{customer_id}"),
        InlineKeyboardButton("❌ REJECT (Fake)", callback_data=f"reject_{customer_id}")
    )
    try:
        bot.send_photo(ADMIN_ID, m.photo[-1].file_id, 
            caption=f"💸 *PAYMENT PROOF RECEIVED*\nFrom: {customer_name}\nCustomer Chat ID: `{customer_id}`\nOrder: {order_info}\n\nCheck your OPay 7045816469 - Did you receive it?\n👇 Click to approve or reject",
            parse_mode="Markdown", reply_markup=markup)
    except Exception as e:
        print(e)

@bot.callback_query_handler(func=lambda call: True)
def handle_approve_reject(call):
    if call.from_user.id != ADMIN_ID:
        bot.answer_callback_query(call.id, "Only owner can approve!")
        return
    action, customer_id_str = call.data.split("_")
    customer_id = int(customer_id_str)
    if action == "approve":
        bot.send_message(customer_id, "✅ *PAYMENT CONFIRMED!* \n\nThanks! We have received your payment to OPay 7045816469 (Promise Emeka).\n\n🚚 Your order is being packaged and will be shipped today!\n\nWe appreciate you shopping with THE7THONE 🖤")
        bot.edit_message_caption(f"✅ *APPROVED* - Payment confirmed for {customer_id}\nCustomer notified.", call.message.chat.id, call.message.message_id, parse_mode="Markdown")
        bot.answer_callback_query(call.id, "Approved!")
    elif action == "reject":
        bot.send_message(customer_id, "❌ *PAYMENT NOT RECEIVED*\n\nBoss, we checked OPay 7045816469 (Promise Emeka) and we didn't see your payment yet.\n\nPlease:\n1. Check if you sent to correct number: 7045816469\n2. Wait 2 mins for network\n3. Send clearer screenshot with transaction ID\n\nOr contact support if you have proof.")
        bot.edit_message_caption(f"❌ *REJECTED* - Fake/not received for {customer_id}\nCustomer notified to recheck.", call.message.chat.id, call.message.message_id, parse_mode="Markdown")
        bot.answer_callback_query(call.id, "Rejected!")

if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    bot.infinity_polling()
