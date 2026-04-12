from aiogram import Router, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from db.sqlite import connect

router = Router()


# =========================
# 🎒 КЛАВИАТУРА ИНВЕНТАРЯ
# =========================
def inventory_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🦴 Кости", callback_data="inv_bones")],
        [InlineKeyboardButton(text="🧴 Бутылки", callback_data="inv_bottles")],
        [InlineKeyboardButton(text="🌫 Пыль", callback_data="inv_dust")],
        [InlineKeyboardButton(text="🧱 Кирпичи", callback_data="inv_bricks")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="menu")]
    ])


# =========================
# 📦 ОТКРЫТИЕ ИНВЕНТАРЯ
# =========================
@router.message(commands=["inventory", "inv"])
async def inventory(message: types.Message):
    conn = connect()
    cur = conn.cursor()

    user = cur.execute("""
        SELECT bones, bottles, dust, bricks
        FROM users WHERE user_id=?
    """, (message.from_user.id,)).fetchone()

    conn.close()

    if not user:
        await message.answer("❌ Ты не зарегистрирован. /start")
        return

    bones, bottles, dust, bricks = user

    text = (
        "🎒 <b>Твой инвентарь:</b>\n\n"
        f"🦴 Кости: {bones}\n"
        f"🧴 Бутылки: {bottles}\n"
        f"🌫 Пыль: {dust}\n"
        f"🧱 Кирпичи: {bricks}\n"
    )

    await message.answer(text, reply_markup=inventory_kb(), parse_mode="HTML")


# =========================
# 🦴 КОСТИ
# =========================
@router.callback_query(F.data == "inv_bones")
async def bones_menu(call: types.CallbackQuery):
    conn = connect()
    cur = conn.cursor()

    bones = cur.execute(
        "SELECT bones FROM users WHERE user_id=?",
        (call.from_user.id,)
    ).fetchone()[0]

    conn.close()

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="♻ Переработать → Пыль (1:1)", callback_data="bones_to_dust")],
        [InlineKeyboardButton(text="💰 Продать (1 = 5💰)", callback_data="bones_sell")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="inv")]
    ])

    await call.message.edit_text(
        f"🦴 <b>Кости</b>\n\nКоличество: {bones}",
        reply_markup=kb,
        parse_mode="HTML"
    )


# =========================
# 🧴 БУТЫЛКИ
# =========================
@router.callback_query(F.data == "inv_bottles")
async def bottles_menu(call: types.CallbackQuery):
    conn = connect()
    cur = conn.cursor()

    bottles = cur.execute(
        "SELECT bottles FROM users WHERE user_id=?",
        (call.from_user.id,)
    ).fetchone()[0]

    conn.close()

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⭐ Использовать (+рейтинг)", callback_data="bottle_use")],
        [InlineKeyboardButton(text="💰 Продать (1 = 10💰)", callback_data="bottle_sell")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="inv")]
    ])

    await call.message.edit_text(
        f"🧴 <b>Бутылки</b>\n\nКоличество: {bottles}",
        reply_markup=kb,
        parse_mode="HTML"
    )


# =========================
# 🌫 ПЫЛЬ
# =========================
@router.callback_query(F.data == "inv_dust")
async def dust_menu(call: types.CallbackQuery):
    conn = connect()
    cur = conn.cursor()

    dust = cur.execute(
        "SELECT dust FROM users WHERE user_id=?",
        (call.from_user.id,)
    ).fetchone()[0]

    conn.close()

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🌳 Удобрить дерево (+рост)", callback_data="dust_tree")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="inv")]
    ])

    await call.message.edit_text(
        f"🌫 <b>Пыль</b>\n\nКоличество: {dust}",
        reply_markup=kb,
        parse_mode="HTML"
    )


# =========================
# 🧱 КИРПИЧИ
# =========================
@router.callback_query(F.data == "inv_bricks")
async def bricks_menu(call: types.CallbackQuery):
    conn = connect()
    cur = conn.cursor()

    bricks = cur.execute(
        "SELECT bricks FROM users WHERE user_id=?",
        (call.from_user.id,)
    ).fetchone()[0]

    conn.close()

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💰 Продать (1 = 25💰)", callback_data="brick_sell")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="inv")]
    ])

    await call.message.edit_text(
        f"🧱 <b>Кирпичи</b>\n\nКоличество: {bricks}",
        reply_markup=kb,
        parse_mode="HTML"
    )
