from db.sqlite import create_user

def register(bot):

    @bot.message_handler(commands=["start"])
    def start(m):
        create_user(m.from_user.id)
        bot.send_message(m.chat.id, "👋 Добро пожаловать!")
