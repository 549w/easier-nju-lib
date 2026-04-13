from pydantic import BaseModel
from typing import List, Optional

from crawler.models import Book, Item

class ItemResponse(BaseModel):
    """
    条目返回类
    """
    item_id: str
    call_no: str
    barcode: str
    current_location_code: Optional[int]
    process_type_code: Optional[int]
    circulation_attribute_code: Optional[str]

class BookResponse(BaseModel):
    """
    图书返回类
    """
    book_id: int
    title: str
    author: str
    publisher: str
    isbn: str
    multi_version_num: Optional[int]
    cover: Optional[str]
    items: List[ItemResponse]
    abstract: Optional[str]
    language_code: Optional[str]

class SearchResponse(BaseModel):
    """
    搜索返回类
    """
    total: int
    books: List[BookResponse]