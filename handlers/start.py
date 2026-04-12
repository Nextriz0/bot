from aiogram import Router, types
from db.sqlite import connect

router = Router()

@router.message()
async def start(message: types.Message):
    conn = connect()
    cur = conn.cursor()

    user = cur.execute("SELECT user_id FROM users WHERE user_id=?",
                       (message.from_user.id,)).fetchone()

    if not user:
        cur.execute("""
        INSERT INTO users (user_id, username)
        VALUES (?, ?)
        """, (message.from_user.id, message.from_user.username))
        conn.commit()

    conn.close()

    await message.answer(
        "👋 Добро пожаловать в игру!\n\nИспользуй меню для начала."
    )
