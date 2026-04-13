import sqlite3

def init_db():
    conn = sqlite3.connect("bot.db")
    cur = conn.cursor()

    cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    money INTEGER DEFAULT 0,
    bones INTEGER DEFAULT 0,
    bottles INTEGER DEFAULT 0,
    dust INTEGER DEFAULT 0,
    tree INTEGER DEFAULT 0,
    last_tree INTEGER DEFAULT 0,
    last_daily INTEGER DEFAULT 0,
    messages INTEGER DEFAULT 0
)
""")

    conn.commit()
    conn.close()


def get_user(user_id):
    conn = sqlite3.connect("bot.db")
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    user = cur.fetchone()

    if not user:
        cur.execute("INSERT INTO users (user_id) VALUES (?)", (user_id,))
        conn.commit()
        return (user_id, 0, 0, 0, 0)

    conn.close()
    return user


def update(user_id, field, value):
    conn = sqlite3.connect("bot.db")
    cur = conn.cursor()

    cur.execute(f"UPDATE users SET {field}=? WHERE user_id=?", (value, user_id))
    conn.commit()
    conn.close()
