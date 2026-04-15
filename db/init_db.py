import sqlite3

def init_db(
        conn: sqlite3.Connection,
):
    with open("db/schema.sql", 'r', encoding="utf-8") as f:
        conn.executescript(f.read())