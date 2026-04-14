import sqlite3
from fastapi import FastAPI
from fastapi.responses import FileResponse
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
        max_uses INTEGER DEFAULT 1,
        used INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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

@app.get("/", response_class=FileResponse)
async def serve_index():
    return FileResponse("index.html")

@app.post("/search/books/nl", response_model=NLSearchResponse)
async def search_books_nl(request: SearchBookRequest):
    semantic_frame = intent_phrase_to_semantic_frame(request.intent_phrase)
    query = semantic_frame_to_query(semantic_frame, request.page, request.rows)
    search_result = book_search(query)
    return NLSearchResponse(query=query, result=search_result)

@app.post("/search/books/query", response_model=BookSearchResponse)
async def search_books_query(query: AdvancedSearchQuery):
    return book_search(query)

@app.get("/search/items/{book_id}", response_model=ItemSearchResponse)
async def search_items(
    book_id: str,
    page: int = 1,
    rows: int = 10,
    sort_type: int = 0
):
    return item_search(book_id, page, rows, sort_type)
