from aiogram import Router, types
import time
import random

from db.sqlite import connect

router = Router()

DIG_COOLDOWN = 30 * 60  # 30 минут

# 🎲 дроп (балансированный)
def generate_loot():
    money = random.randint(20, 120)
    bones = random.randint(0, 3)
    bottles = random.randint(0, 2)

    # редкий кирпич
    bricks = 1 if random.randint(1, 100) <= 8 else 0  # 8%

    return money, bones, bottles, bricks


@router.message(commands=["dig"])
async def dig(message: types.Message):
    user_id = message.from_user.id
    now = int(time.time())

    conn = connect()
    cur = conn.cursor()

    user = cur.execute(
        "SELECT money, bones, bottles, bricks, last_dig FROM users WHERE user_id=?",
        (user_id,)
    ).fetchone()

    if not user:
        await message.answer("❌ Ты не зарегистрирован. Напиши /start")
        return

    money, bones, bottles, bricks, last_dig = user

    # ⛔ кулдаун
    if now - last_dig < DIG_COOLDOWN:
        remaining = DIG_COOLDOWN - (now - last_dig)
        minutes = remaining // 60
        await message.answer(f"⏳ Подожди {minutes} мин. перед следующим копанием.")
        return

    # 🎲 лут
    add_money, add_bones, add_bottles, add_bricks = generate_loot()

    money += add_money
    bones += add_bones
    bottles += add_bottles
    bricks += add_bricks

    # 💾 обновление
    cur.execute("""
        UPDATE users
        SET money=?, bones=?, bottles=?, bricks=?, last_dig=?
        WHERE user_id=?
    """, (money, bones, bottles, bricks, now, user_id))

    conn.commit()
    conn.close()

    # 🎉 ответ игроку
    text = "⛏ Ты покопал и нашёл:\n\n"
    text += f"💰 +{add_money} монет\n"
    text += f"🦴 +{add_bones} костей\n"
    text += f"🧴 +{add_bottles} бутылок\n"

    if add_bricks:
        text += f"🧱 +{add_bricks} кирпич (редко!)\n"

    text += "\n⌛ Кулдаун: 30 минут"

    await message.answer(text)
