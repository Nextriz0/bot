from db.sqlite import get_user

def register(bot):

    @bot.message_handler(commands=["profile"])
    def profile(m):
        u = get_user(m.from_user.id)

        bot.send_message(m.chat.id,
        f"""👤 Профиль

💰 {u[1]}
🦴 {u[2]}
🧴 {u[3]}
🌫 {u[4]}
🌳 {u[5]} м
⭐ {u[7]}
""")
