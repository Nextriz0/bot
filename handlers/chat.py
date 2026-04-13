from db.sqlite import get_user, update

def register(bot):

    @bot.message_handler(func=lambda m: True)
    def chat(m):
        u = get_user(m.from_user.id)
        update(m.from_user.id, "messages", u[8] + 1)
