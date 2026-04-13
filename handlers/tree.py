import time
import random
from telebot import types
from db.sqlite import get_user, update

COOLDOWN = 14400  # 4 часа

def register(bot):

    @bot.message_handler(commands=['tree'])
    def tree(m):
        markup = types.InlineKeyboardMarkup()

        markup.add(
            types.InlineKeyboardButton("💧 Полить", callback_data="tree_water"),
            types.InlineKeyboardButton("🌱 Удобрить", callback_data="tree_fert")
        )

        bot.send_message(m.chat.id, "🌳 Дерево", reply_markup=markup)


    @bot.callback_query_handler(func=lambda c: c.data.startswith("tree_"))
    def tree_actions(call):
        u = get_user(call.from_user.id)
        now = int(time.time())

        # 💧 Полив
        if call.data == "tree_water":
            if now - u[6] < COOLDOWN:
                return bot.answer_callback_query(call.id, "⏳ Рано")

            grow = random.randint(1, 5)
            update(call.from_user.id, "tree", u[5] + grow)
            update(call.from_user.id, "last_tree", now)

            bot.answer_callback_query(call.id, f"🌳 +{grow}м")

        # 🌱 Удобрение
        if call.data == "tree_fert":
            if u[4] < 1:
                return bot.answer_callback_query(call.id, "Нет пыли")

            grow = random.randint(2, 6)
            update(call.from_user.id, "dust", u[4] - 1)
            update(call.from_user.id, "tree", u[5] + grow)

            bot.answer_callback_query(call.id, f"🌱 +{grow}м")
