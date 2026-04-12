from game.economy import dig

def register(bot):

    @bot.message_handler(commands=["dig"])
    def dig_cmd(m):
        res = dig(m.from_user.id)

        bot.send_message(m.chat.id,
        f"⛏ Добыча:\n💰+{res[0]} 🦴+{res[1]} 🧴+{res[2]}")
