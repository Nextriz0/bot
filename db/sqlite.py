import sqlite3
from config import DB_PATH

def connect():
    return sqlite3.connect(DB_PATH)

def init_db():
    conn = connect()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        money INTEGER DEFAULT 0,
        bones INTEGER DEFAULT 0,
        bottles INTEGER DEFAULT 0,
        dust INTEGER DEFAULT 0,
        bricks INTEGER DEFAULT 0,
        tree_growth INTEGER DEFAULT 0,
        rating INTEGER DEFAULT 0,
        last_daily INTEGER DEFAULT 0,
        last_dig INTEGER DEFAULT 0,
        last_tree INTEGER DEFAULT 0
    )
    """)

    conn.commit()
    conn.close()
