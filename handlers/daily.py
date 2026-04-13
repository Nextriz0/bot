import time
from db.sqlite import get_user, update

COOLDOWN = 86400

def register(bot):

    @bot.message_handler(commands=['daily'])
    def daily(m):
        u = get_user(m.from_user.id)
        now = int(time.time())

        if now - u[7] < COOLDOWN:
            return bot.send_message(m.chat.id, "⏳ Уже забирал")

        update(m.from_user.id, "money", u[1] + 500)
        update(m.from_user.id, "last_daily", now)

        bot.send_message(m.chat.id, "🎁 +500 💰")
