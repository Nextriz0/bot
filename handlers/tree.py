from telebot import types
from game.tree import water_tree, fertilize
from db.sqlite import get_user

def register(bot):

    @bot.message_handler(commands=["tree"])
    def tree(m):

        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton("💧 Полить", callback_data="water"),
            types.InlineKeyboardButton("🌫 Удобрить", callback_data="fert")
        )

        u = get_user(m.from_user.id)

        bot.send_message(m.chat.id, f"🌳 {u[5]} м", reply_markup=markup)

    @bot.callback_query_handler(func=lambda c: True)
    def cb(call):

        if call.data == "water":
            res = water_tree(call.from_user.id)
            bot.answer_callback_query(call.id, f"+{res} м" if res else "⏱ рано")

        if call.data == "fert":
            ok = fertilize(call.from_user.id)
            bot.answer_callback_query(call.id, "🌫 использовано" if ok else "нет пыли")
