import sqlite3
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional

from service import (
    intent_phrase_to_semantic_frame,
    semantic_frame_to_query,
    book_search,
    item_search
)
from schemas import (
    SemanticFrameModel,
    BookSearchResponse,
    ItemSearchResponse
)
from crawler.payloads import AdvancedSearchQuery

from exceptions import (
    LLMError
)

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

class SearchBookRequest(BaseModel):
    intent_phrase: str
    page: int = 1
    rows: int = 10

class NLSearchResponse(BaseModel):
    query: AdvancedSearchQuery
    result: BookSearchResponse

app = FastAPI()

app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

@app.get("/", response_class=FileResponse)
async def serve_index():
    return FileResponse("frontend/index.html")

@app.post("/search/books/llm_query", response_model=NLSearchResponse)
async def search_books_normal_query(request: SearchBookRequest):
    # 验证搜索词长度不超过50字
    if len(request.intent_phrase.strip()) > 50:
        raise HTTPException(
            status_code=400,
            detail="搜索词不能超过50个字"
        )
    
    try:
        semantic_frame: SemanticFrameModel = intent_phrase_to_semantic_frame(
            request.intent_phrase.strip()
            )
        #print(semantic_frame)
    except LLMError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
            )

    query = semantic_frame_to_query(semantic_frame, request.page, request.rows)
    search_result = book_search(query)
    return NLSearchResponse(query=query, result=search_result)

@app.post("/search/books/normal_query", response_model=BookSearchResponse)
async def search_books_llm_query(query: AdvancedSearchQuery):
    return book_search(query)

@app.get("/search/items/{book_id}", response_model=ItemSearchResponse)
async def search_items(
    book_id: str,
    page: int = 1,
    rows: int = 10,
    sort_type: int = 0
):
    return item_search(book_id, page, rows, sort_type)
