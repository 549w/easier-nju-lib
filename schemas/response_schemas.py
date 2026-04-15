"""响应相关的Schema定义"""
from pydantic import BaseModel
from typing import List


class ItemResponse(BaseModel):
    """条目返回类"""
    item_id: int|None
    call_no: str|None
    barcode: str|None
    current_location_code: int | None
    current_location_name: str | None
    process_type_code: int | None
    process_type_name: str | None
    circulation_attribute_code: str | None
    circulation_attribute_name: str | None
    campus_id: int | None


class BookResponse(BaseModel):
    """图书返回类"""
    book_id: int
    title: str
    author: str|None
    publisher: str|None
    isbn: str|None
    multi_version_num: int|None
    cover: str | None
    items: List[ItemResponse]
    abstract: str | None
    language_code: str | None
    total_count: int | None
    on_shelf_count: int | None


class BookSearchResponse(BaseModel):
    """搜索返回类"""
    total: int
    books: List[BookResponse]


class ItemSearchResponse(BaseModel):
    """条目搜索返回类"""
    total: int
    items: List[ItemResponse]
