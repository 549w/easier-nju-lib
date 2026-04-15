import sqlite3
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from api.search_api import router as search_router

from db.init_db import init_db
from db.connection import get_connection

@asynccontextmanager
async def lifespan(
    app: FastAPI
):
    conn = get_connection()
    init_db(conn)
    conn.close
    yield

app = FastAPI(lifespan=lifespan)

# 挂载静态文件
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

# 注册路由
app.include_router(search_router)


@app.get("/", response_class=FileResponse)
async def serve_index():
    """提供前端首页"""
    return FileResponse("frontend/index.html")
