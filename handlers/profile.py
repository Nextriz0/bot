from db import get_user

def register(bot):
    @bot.message_handler(commands=['profile'])
    def profile(m):
        u = get_user(m.from_user.id)

        text = f"""
👤 Профиль

💰 Деньги: {u[1]}
🦴 Кости: {u[2]}
🧴 Банки: {u[3]}
🌫 Пыль: {u[4]}
"""

        bot.send_message(m.chat.id, text)
