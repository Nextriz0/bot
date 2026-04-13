def register(bot):
    @bot.message_handler(commands=['start'])
    def start(m):
        bot.send_message(m.chat.id, "👋 Добро пожаловать в RPG бот!")
