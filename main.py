import os
import random
import threading
import time
import telebot
from flask import Flask

# ══════════════════════════════════════════════
#   TOKEN (Environment Variable থেকে নিবে)
# ══════════════════════════════════════════════
TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")
CHANNEL_ID = "-1003758064245"  # আপনার চ্যানেল আইডি

app = Flask(__name__)
bot = telebot.TeleBot(TOKEN)

BINS = [
    {"bin": "533985", "currency": "CAD"},
    {"bin": "461126", "currency": "CAD"},
    {"bin": "428313", "currency": "AUD"},
    {"bin": "457824", "currency": "AUD"},
    {"bin": "432465", "currency": "AUD"},
    {"bin": "373778", "currency": "USD"},
    {"bin": "377935", "currency": "USD"},
    {"bin": "375163", "currency": "USD"},
    {"bin": "435880", "currency": "USD"},
    {"bin": "491277", "currency": "USD"},
    {"bin": "511332", "currency": "USD"},
    {"bin": "520356", "currency": "USD"},
    {"bin": "409758", "currency": "USD"},
    {"bin": "525362", "currency": "USD"},
    {"bin": "451129", "currency": "USD"},
    {"bin": "434340", "currency": "USD"},
    {"bin": "426370", "currency": "USD"},
    {"bin": "411810", "currency": "USD"},
    {"bin": "403446", "currency": "USD"},
    {"bin": "533621", "currency": "USD"},
    {"bin": "446317", "currency": "USD"},
    {"bin": "545660", "currency": "USD"},
    {"bin": "516612", "currency": "USD"},
    {"bin": "484718", "currency": "USD"},
    {"bin": "485246", "currency": "USD"},
    {"bin": "402372", "currency": "USD"},
    {"bin": "457851", "currency": "USD"},
]

CAD_TO_USD = 0.73
AUD_TO_USD = 0.65


@app.route("/")
def index():
    return "✅ Bot is running!", 200


@app.route("/health")
def health():
    return "OK", 200


def chance(percent):
    return random.random() * 100 < percent


def random_balance():
    if chance(90):
        return round(random.uniform(0.10, 49.99), 2)
    return round(random.uniform(50.00, 250.00), 2)


def to_usd(balance, currency):
    if currency == "CAD":
        return balance * CAD_TO_USD
    if currency == "AUD":
        return balance * AUD_TO_USD
    return balance


def generate_listing():
    entry = random.choice(BINS)
    xx = str(random.randint(0, 99)).zfill(2)
    full_bin = entry["bin"] + xx
    currency = entry["currency"]
    balance = random_balance()
    usd_bal = to_usd(balance, currency)
    price = round(usd_bal * 0.36, 2)
    paypal = "Yes" if chance(10) else "No"
    google = "Yes" if chance(10) else "No"
    registered = "True" if chance(25) else "False"
    return (
        f"📢 <b>New Listing Added!</b>\n\n"
        f" <b>• Card BIN</b>: <code>{full_bin}</code>\n"
        f" <b>• Balance</b>: $<code>{balance:.2f}</code>\n"
        f" <b>• Card Type</b>: <code>{currency}</code>\n"
        f"<b>• Price</b>: $<code>{price:.2f}</code>\n"
        f"<b>• Rate</b>: <code>36.0%</code>\n"
        f"<b>• Used PayPal</b>: {paypal}\n"
        f"<b>• Used Google</b>: {google}\n"
        f"<b>• Registered</b>: {registered}\n\n"
        f"<b>• 🛒Purchase</b> ➔ @Vanilacard_bot"
    )


def post_cycle():
    count = random.randint(1, 3)
    print(f"📤 Sending {count} listing(s)...", flush=True)
    for i in range(count):
        try:
            bot.send_message(CHANNEL_ID, generate_listing(), parse_mode="HTML")
            print(f"✅ Posted {i+1}/{count}", flush=True)
        except Exception as e:
            print(f"❌ Failed {i+1}: {e}", flush=True)
        if i < count - 1:
            delay = random.randint(15, 45)
            print(f"⏳ Waiting {delay}s...", flush=True)
            time.sleep(delay)


def posting_loop():
    while True:
        post_cycle()
        print("⏰ Next in 5 min...", flush=True)
        time.sleep(5 * 60)


@bot.message_handler(commands=["start"])
def handle_start(message):
    try:
        bot.send_message(message.chat.id, "Im ready to listings✅")
        print(f"✅ /start → {message.chat.id}", flush=True)
    except Exception as e:
        print(f"❌ /start error: {e}", flush=True)


if __name__ == "__main__":
    print("✅ Bot starting...", flush=True)

    threading.Thread(target=posting_loop, daemon=True).start()

    threading.Thread(
        target=bot.infinity_polling,
        kwargs={"timeout": 30, "long_polling_timeout": 30},
        daemon=True,
    ).start()

    port = int(os.environ.get("PORT", 10000))
    print(f"🌐 Flask server on port {port}", flush=True)
    app.run(host="0.0.0.0", port=port)
