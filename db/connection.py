import sqlite3

def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect("db.sqlite3")
    conn.row_factory = sqlite3.Row
    return conn