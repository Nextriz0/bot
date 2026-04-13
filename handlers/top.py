from db.sqlite import sqlite3

def get_top(field):
    conn = sqlite3.connect("bot.db")
    cur = conn.cursor()

    cur.execute(f"SELECT user_id, {field} FROM users ORDER BY {field} DESC LIMIT 10")
    data = cur.fetchall()

    conn.close()
    return data


def register(bot):

    @bot.message_handler(commands=['top'])
    def top(m):
        text = "🏆 Топ по деньгам:\n\n"

        data = get_top("money")

        for i, user in enumerate(data, 1):
            text += f"{i}. {user[0]} — {user[1]}💰\n"

        bot.send_message(m.chat.id, text)
