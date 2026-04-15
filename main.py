import sqlite3
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from api.search import router as search_router

# 数据库初始化
conn = sqlite3.connect("data.db")
cursor = conn.cursor()
cursor.executescript("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT UNIQUE,
        password_hash TEXT,
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
    CREATE TABLE IF NOT EXISTS invite_codes (
        code TEXT PRIMARY KEY,
        quota_bonus INTEGER NOT NULL,
        used INTEGER DEFAULT 0
    );
    CREATE TABLE IF NOT EXISTS usage_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        email TEXT NOT NULL,
        user_prompt TEXT NOT NULL,
        prompt_tokens INTEGER NOT NULL,
        completion_tokens INTEGER NOT NULL,
        finish_reason TEXT NOT NULL,
        completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        completion_id TEXT NOT NULL,
        completion_model TEXT NOT NULL
    );
""")

app = FastAPI()

# 挂载静态文件
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

# 注册路由
app.include_router(search_router)


@app.get("/", response_class=FileResponse)
async def serve_index():
    """提供前端首页"""
    return FileResponse("frontend/index.html")
