import telebot
import time
import sqlite3
import random

TOKEN = "PASTE_YOUR_TOKEN_HERE"
bot = telebot.TeleBot(TOKEN)

# =========================
# DB
# =========================
conn = sqlite3.connect("game.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    money INTEGER DEFAULT 0,
    bones INTEGER DEFAULT 0,
    bottles INTEGER DEFAULT 0,
    dust INTEGER DEFAULT 0,
    bricks INTEGER DEFAULT 0,
    tree INTEGER DEFAULT 0,
    rating INTEGER DEFAULT 0,
    last_dig INTEGER DEFAULT 0,
    last_daily INTEGER DEFAULT 0
)
""")
conn.commit()


# =========================
# REGISTER USER
# =========================
def get_user(user):
    cur.execute("SELECT * FROM users WHERE user_id=?", (user.id,))
    data = cur.fetchone()

    if not data:
        cur.execute("""
        INSERT INTO users (user_id, username)
        VALUES (?, ?)
        """, (user.id, user.username))
        conn.commit()


# =========================
# MENU
# =========================
def menu_kb():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("👤 Профиль", "🎒 Инвентарь")
    markup.row("⛏ Копать", "💰 Бонус")
    return markup


# =========================
# START
# =========================
@bot.message_handler(commands=["start"])
def start(message):
    get_user(message.from_user)
    bot.send_message(message.chat.id, "👋 Добро пожаловать в игру!", reply_markup=menu_kb())


# =========================
# PROFILE
# =========================
@bot.message_handler(func=lambda m: m.text == "👤 Профиль")
def profile(message):
    get_user(message.from_user)

    cur.execute("SELECT money, bones, bottles, dust, tree, rating FROM users WHERE user_id=?",
                (message.from_user.id,))
    u = cur.fetchone()

    bot.send_message(message.chat.id,
        f"""👤 Профиль

💰 {u[0]}
🦴 {u[1]}
🧴 {u[2]}
🌫 {u[3]}
🌳 {u[4]}
⭐ {u[5]}
""",
    )


# =========================
# DIG SYSTEM
# =========================
@bot.message_handler(func=lambda m: m.text == "⛏ Копать")
def dig(message):
    get_user(message.from_user)

    cur.execute("SELECT last_dig FROM users WHERE user_id=?", (message.from_user.id,))
    last = cur.fetchone()[0]

    now = int(time.time())

    if now - last < 1800:
        wait = (1800 - (now - last)) // 60
        bot.send_message(message.chat.id, f"⏳ Подожди {wait} мин")
        return

    money = random.randint(20, 120)
    bones = random.randint(0, 3)
    bottles = random.randint(0, 2)
    bricks = 1 if random.randint(1, 100) < 8 else 0

    cur.execute("""
        UPDATE users
        SET money = money + ?,
            bones = bones + ?,
            bottles = bottles + ?,
            bricks = bricks + ?,
            last_dig = ?
        WHERE user_id=?
    """, (money, bones, bottles, bricks, now, message.from_user.id))

    conn.commit()

    bot.send_message(message.chat.id,
        f"""⛏ Ты выкопал:

💰 +{money}
🦴 +{bones}
🧴 +{bottles}
🧱 +{bricks if bricks else 0}
"""
    )


# =========================
# DAILY BONUS
# =========================
@bot.message_handler(func=lambda m: m.text == "💰 Бонус")
def daily(message):
    get_user(message.from_user)

    cur.execute("SELECT last_daily FROM users WHERE user_id=?", (message.from_user.id,))
    last = cur.fetchone()[0]

    now = int(time.time())

    if now - last < 86400:
        bot.send_message(message.chat.id, "⏳ Уже забрал бонус")
        return

    cur.execute("""
        UPDATE users
        SET money = money + 500,
            last_daily = ?
        WHERE user_id=?
    """, (now, message.from_user.id))

    conn.commit()

    bot.send_message(message.chat.id, "🎁 +500 💰")


# =========================
# INVENTORY
# =========================
@bot.message_handler(func=lambda m: m.text == "🎒 Инвентарь")
def inv(message):
    get_user(message.from_user)

    cur.execute("SELECT bones, bottles, dust, bricks FROM users WHERE user_id=?",
                (message.from_user.id,))
    b, bo, d, br = cur.fetchone()

    bot.send_message(message.chat.id,
        f"""🎒 Инвентарь

🦴 {b}
🧴 {bo}
🌫 {d}
🧱 {br}
"""
    )


# =========================
# RUN
# =========================
print("BOT STARTED")
bot.infinity_polling()
