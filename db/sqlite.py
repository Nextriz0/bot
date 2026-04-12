import sqlite3

conn = sqlite3.connect("game.db", check_same_thread=False)
cur = conn.cursor()

def init_db():
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        money INTEGER DEFAULT 0,
        bones INTEGER DEFAULT 0,
        bottles INTEGER DEFAULT 0,
        dust INTEGER DEFAULT 0,
        tree REAL DEFAULT 0,
        rating INTEGER DEFAULT 0,
        daily_rating INTEGER DEFAULT 0,
        last_water INTEGER DEFAULT 0
    )
    """)
    conn.commit()

def get_user(user_id):
    cur.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    return cur.fetchone()

def create_user(user_id):
    if not get_user(user_id):
        cur.execute("INSERT INTO users (user_id) VALUES (?)", (user_id,))
        conn.commit()

def update(user_id, field, value):
    cur.execute(f"UPDATE users SET {field}=? WHERE user_id=?", (value, user_id))
    conn.commit()
