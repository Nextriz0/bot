from telebot import types
from db.sqlite import get_user, update
from game.economy import dig

# ---------- OPEN INVENTORY ----------
def register(bot):

    @bot.message_handler(commands=["inventory", "inv"])
    def inv(m):
        u = get_user(m.from_user.id)

        markup = types.InlineKeyboardMarkup(row_width=2)

        markup.add(
            types.InlineKeyboardButton(f"🦴 Кости ({u[2]})", callback_data="inv_bones"),
            types.InlineKeyboardButton(f"🧴 Банки ({u[3]})", callback_data="inv_bottles"),
        )

        markup.add(
            types.InlineKeyboardButton(f"🌫 Пыль ({u[4]})", callback_data="inv_dust"),
        )

        bot.send_message(m.chat.id, "🎒 Инвентарь:", reply_markup=markup)

    # ---------- CALLBACK ROUTER ----------
    @bot.callback_query_handler(func=lambda c: c.data.startswith("inv_"))
    def inv_router(call):
        u = get_user(call.from_user.id)

        if call.data == "inv_bones":
            show_bones(bot, call, u)

        if call.data == "inv_bottles":
            show_bottles(bot, call, u)

        if call.data == "inv_dust":
            show_dust(bot, call, u)


# ---------- BONES ----------
def show_bones(bot, call, u):
    markup = types.InlineKeyboardMarkup()

    markup.add(
        types.InlineKeyboardButton("♻ Переработать", callback_data="bones_recycle"),
        types.InlineKeyboardButton("💰 Продать", callback_data="bones_sell"),
        types.InlineKeyboardButton("🔙 Назад", callback_data="inv_back")
    )

    bot.edit_message_text(
        f"🦴 Кости: {u[2]}",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=markup
    )


# ---------- BOTTLES ----------
def show_bottles(bot, call, u):
    markup = types.InlineKeyboardMarkup()

    markup.add(
        types.InlineKeyboardButton("⭐ Использовать", callback_data="bottle_use"),
        types.InlineKeyboardButton("💰 Продать", callback_data="bottle_sell"),
        types.InlineKeyboardButton("🔙 Назад", callback_data="inv_back")
    )

    bot.edit_message_text(
        f"🧴 Банки: {u[3]}",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=markup
    )


# ---------- DUST ----------
def show_dust(bot, call, u):
    markup = types.InlineKeyboardMarkup()

    markup.add(
        types.InlineKeyboardButton("🌳 Удобрить дерево", callback_data="dust_fert"),
        types.InlineKeyboardButton("🔙 Назад", callback_data="inv_back")
    )

    bot.edit_message_text(
        f"🌫 Пыль: {u[4]}",
        call.message.chat.id,
        call.message.message_id,
        reply_markup=markup
    )


# ---------- ACTIONS ----------
def register_actions(bot):

    @bot.callback_query_handler(func=lambda c: c.data == "inv_back")
    def back(call):
        inv(call.message)  # возвращаем меню


    # 🦴 BONES
    @bot.callback_query_handler(func=lambda c: c.data == "bones_recycle")
    def recycle(call):
        u = get_user(call.from_user.id)

        if u[2] < 1:
            return bot.answer_callback_query(call.id, "нет костей")

        update(call.from_user.id, "bones", u[2] - 1)
        update(call.from_user.id, "dust", u[4] + 1)

        bot.answer_callback_query(call.id, "♻ +1 пыль")


    @bot.callback_query_handler(func=lambda c: c.data == "bones_sell")
    def sell_bones(call):
        u = get_user(call.from_user.id)

        if u[2] < 1:
            return bot.answer_callback_query(call.id, "нет костей")

        update(call.from_user.id, "bones", u[2] - 1)
        update(call.from_user.id, "money", u[1] + 50)

        bot.answer_callback_query(call.id, "💰 продано +50")


    # 🧴 BOTTLES
    @bot.callback_query_handler(func=lambda c: c.data == "bottle_use")
    def use_bottle(call):
        u = get_user(call.from_user.id)

        if u[3] < 1:
            return bot.answer_callback_query(call.id, "нет банок")

        update(call.from_user.id, "bottles", u[3] - 1)
        update(call.from_user.id, "rating", u[7] + 1)

        bot.answer_callback_query(call.id, "⭐ +1 рейтинг")


    @bot.callback_query_handler(func=lambda c: c.data == "bottle_sell")
    def sell_bottle(call):
        u = get_user(call.from_user.id)

        if u[3] < 1:
            return bot.answer_callback_query(call.id, "нет банок")

        update(call.from_user.id, "bottles", u[3] - 1)
        update(call.from_user.id, "money", u[1] + 100)

        bot.answer_callback_query(call.id, "💰 +100")


    # 🌫 DUST
    @bot.callback_query_handler(func=lambda c: c.data == "dust_fert")
    def fertilize(call):
        u = get_user(call.from_user.id)

        if u[4] < 1:
            return bot.answer_callback_query(call.id, "нет пыли")

        update(call.from_user.id, "dust", u[4] - 1)

        bot.answer_callback_query(call.id, "🌳 дерево усилено")
