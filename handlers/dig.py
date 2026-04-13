import random
from db import get_user, update

def register(bot):
    @bot.message_handler(commands=['dig'])
    def dig(m):
        u = get_user(m.from_user.id)

        bones = random.randint(1, 3)
        bottles = random.randint(0, 1)
        money = random.randint(20, 50)

        update(m.from_user.id, "bones", u[2] + bones)
        update(m.from_user.id, "bottles", u[3] + bottles)
        update(m.from_user.id, "money", u[1] + money)

        bot.send_message(
            m.chat.id,
            f"⛏ Добыча:\n🦴 {bones} | 🧴 {bottles} | 💰 {money}"
        )
