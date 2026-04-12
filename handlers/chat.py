from game.rating import add_chat_point

def register(bot):

    @bot.message_handler(func=lambda m: True)
    def chat(m):
        if m.text and not m.text.startswith("."):
            add_chat_point(m.from_user.id)
