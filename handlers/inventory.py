from telebot import types
from db.sqlite import get_user, update

def register(bot):

    @bot.message_handler(commands=['inventory'])
    def inv(m):
        u = get_user(m.from_user.id)

        markup = types.InlineKeyboardMarkup()

        markup.add(
            types.InlineKeyboardButton(f"🦴 Кости ({u[2]})", callback_data="bones"),
            types.InlineKeyboardButton(f"🧴 Банки ({u[3]})", callback_data="bottles"),
        )

        markup.add(
            types.InlineKeyboardButton(f"🌫 Пыль ({u[4]})", callback_data="dust"),
        )

        bot.send_message(m.chat.id, "🎒 Инвентарь", reply_markup=markup)


    @bot.callback_query_handler(func=lambda c: True)
    def callbacks(call):
        u = get_user(call.from_user.id)

        # 🦴 Кости → пыль
        if call.data == "bones":
            if u[2] > 0:
                update(call.from_user.id, "bones", u[2] - 1)
                update(call.from_user.id, "dust", u[4] + 1)
                bot.answer_callback_query(call.id, "♻ Кость → Пыль")
            else:
                bot.answer_callback_query(call.id, "Нет костей")

        # 🧴 Банки → деньги
        if call.data == "bottles":
            if u[3] > 0:
                update(call.from_user.id, "bottles", u[3] - 1)
                update(call.from_user.id, "money", u[1] + 100)
                bot.answer_callback_query(call.id, "💰 Продано")
            else:
                bot.answer_callback_query(call.id, "Нет банок")

        # 🌫 Пыль
        if call.data == "dust":
            bot.answer_callback_query(call.id, "🌫 Пока без действия")
