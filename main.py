import sqlite3
from fastapi import FastAPI

conn = sqlite3.connect("data.db")
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE,
        password_hash TEXT
        quota INTEGER DEFAULT 5
    );
    CREATE TABLE IF NOT EXISTS email_codes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL,
        code TEXT NOT NULL,
        expire_at TIMESTAMP NOT NULL,
        used INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    CREATE TABLE invite_codes (
        code TEXT PRIMARY KEY,
        quota_bonus INTEGER NOT NULL,
        max_uses INTEGER DEFAULT 1,
        used INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
""")

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/search")
def search(keyword: str):
    return {"keyword": keyword}
