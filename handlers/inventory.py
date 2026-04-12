from aiogram import Router, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from db.sqlite import connect

router = Router()

# =========================
# 🎒 MENU
# =========================
def inventory_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🦴 Кости", callback_data="inv_bones")],
        [InlineKeyboardButton(text="🧴 Бутылки", callback_data="inv_bottles")],
        [InlineKeyboardButton(text="🌫 Пыль", callback_data="inv_dust")],
        [InlineKeyboardButton(text="🧱 Кирпичи", callback_data="inv_bricks")],
    ])


# =========================
# 📦 OPEN INVENTORY
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
        "🎒 <b>Инвентарь:</b>\n\n"
        f"🦴 {bones}\n"
        f"🧴 {bottles}\n"
        f"🌫 {dust}\n"
        f"🧱 {bricks}\n"
    )

    await message.answer(text, reply_markup=inventory_kb(), parse_mode="HTML")


# =========================
# 🦴 BONES MENU
# =========================
@router.callback_query(F.data == "inv_bones")
async def bones_menu(call: types.CallbackQuery):
    conn = connect()
    cur = conn.cursor()

    bones = cur.execute(
        "SELECT bones FROM users WHERE user_id=?",
        (call.from_user.id,)
    ).fetchone()

    conn.close()

    if not bones:
        await call.answer("❌ ошибка")
        return

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="♻ → Пыль", callback_data="bones_to_dust")],
        [InlineKeyboardButton(text="💰 Продать", callback_data="bones_sell")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="inv_back")]
    ])

    await call.message.edit_text(
        f"🦴 Кости: {bones[0]}",
        reply_markup=kb
    )


# =========================
# 🧴 BOTTLES
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
        [InlineKeyboardButton(text="⭐ Использовать", callback_data="bottle_use")],
        [InlineKeyboardButton(text="💰 Продать", callback_data="bottle_sell")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="inv_back")]
    ])

    await call.message.edit_text(
        f"🧴 Бутылки: {bottles}",
        reply_markup=kb
    )


# =========================
# 🌫 DUST
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
        [InlineKeyboardButton(text="🌳 Удобрить", callback_data="dust_tree")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="inv_back")]
    ])

    await call.message.edit_text(
        f"🌫 Пыль: {dust}",
        reply_markup=kb
    )


# =========================
# 🧱 BRICKS
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
        [InlineKeyboardButton(text="💰 Продать", callback_data="brick_sell")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="inv_back")]
    ])

    await call.message.edit_text(
        f"🧱 Кирпичи: {bricks}",
        reply_markup=kb
    )


# =========================
# 🔙 BACK
# =========================
@router.callback_query(F.data == "inv_back")
async def back(call: types.CallbackQuery):
    await call.message.edit_text(
        "🎒 Инвентарь:",
        reply_markup=inventory_kb()
    )


# =========================
# ♻ BONES → DUST
# =========================
@router.callback_query(F.data == "bones_to_dust")
async def bones_to_dust(call: types.CallbackQuery):
    conn = connect()
    cur = conn.cursor()

    bones, dust = cur.execute(
        "SELECT bones, dust FROM users WHERE user_id=?",
        (call.from_user.id,)
    ).fetchone()

    if bones <= 0:
        await call.answer("❌ нет костей")
        return

    cur.execute("""
        UPDATE users
        SET bones=bones-1, dust=dust+1
        WHERE user_id=?
    """, (call.from_user.id,))

    conn.commit()
    conn.close()

    await call.answer("♻ сделано")


# =========================
# 💰 SELL BONES
# =========================
@router.callback_query(F.data == "bones_sell")
async def bones_sell(call: types.CallbackQuery):
    conn = connect()
    cur = conn.cursor()

    bones, money = cur.execute(
        "SELECT bones, money FROM users WHERE user_id=?",
        (call.from_user.id,)
    ).fetchone()

    if bones <= 0:
        await call.answer("❌ нет костей")
        return

    cur.execute("""
        UPDATE users
        SET bones=0, money=money + ?
        WHERE user_id=?
    """, (bones * 5, call.from_user.id))

    conn.commit()
    conn.close()

    await call.answer("💰 продано")


# =========================
# ⭐ BOTTLE USE
# =========================
@router.callback_query(F.data == "bottle_use")
async def bottle_use(call: types.CallbackQuery):
    conn = connect()
    cur = conn.cursor()

    bottles, rating = cur.execute(
        "SELECT bottles, rating FROM users WHERE user_id=?",
        (call.from_user.id,)
    ).fetchone()

    if bottles <= 0:
        await call.answer("❌ нет бутылок")
        return

    cur.execute("""
        UPDATE users
        SET bottles=bottles-1, rating=rating+2
        WHERE user_id=?
    """, (call.from_user.id,))

    conn.commit()
    conn.close()

    await call.answer("⭐ +2")


# =========================
# 🌳 DUST → TREE
# =========================
@router.callback_query(F.data == "dust_tree")
async def dust_tree(call: types.CallbackQuery):
    conn = connect()
    cur = conn.cursor()

    dust, tree = cur.execute(
        "SELECT dust, tree_growth FROM users WHERE user_id=?",
        (call.from_user.id,)
    ).fetchone()

    if dust <= 0:
        await call.answer("❌ нет пыли")
        return

    cur.execute("""
        UPDATE users
        SET dust=dust-1, tree_growth=tree_growth+2
        WHERE user_id=?
    """, (call.from_user.id,))

    conn.commit()
    conn.close()

    await call.answer("🌳 рост")


# =========================
# 🧱 BRICK SELL
# =========================
@router.callback_query(F.data == "brick_sell")
async def brick_sell(call: types.CallbackQuery):
    conn = connect()
    cur = conn.cursor()

    bricks, money = cur.execute(
        "SELECT bricks, money FROM users WHERE user_id=?",
        (call.from_user.id,)
    ).fetchone()

    if bricks <= 0:
        await call.answer("❌ нет кирпичей")
        return

    cur.execute("""
        UPDATE users
        SET bricks=0, money=money + ?
        WHERE user_id=?
    """, (bricks * 25, call.from_user.id))

    conn.commit()
    conn.close()

    await call.answer("💰 продано")
