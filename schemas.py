from pydantic import BaseModel, model_validator
from typing import List, Optional

from crawler.models import Book, Item
from crawler.payloads import (
    CampusID,
    MatchMode,
    Oper,
    SearchField,
)

class SearchItemModel(BaseModel):
    oper: Optional[Oper]
    searchField: SearchField
    matchMode: MatchMode
    searchFieldContent: str

class SemanticFrameModel(BaseModel):
    campusId: List[Optional[CampusID]]
    searchItems: List[SearchItemModel]

    @model_validator(mode="after")
    def check_oper_rule(self):
        if not self.searchItems:
            raise ValueError("searchItems 不能为空")

        if self.searchItems[0].oper is not None:
            raise ValueError("第一个 oper 必须为 None")

        for i in range(1, len(self.searchItems)):
            if self.searchItems[i].oper is None:
                raise ValueError(f"第{i}个 oper 不能为 None")

        return self

class ItemResponse(BaseModel):
    """
    条目返回类
    """
    item_id: int|None
    call_no: str|None
    barcode: str|None
    current_location_code: Optional[int]
    current_location_name: Optional[str]
    process_type_code: Optional[int]
    process_type_name: Optional[str]
    circulation_attribute_code: Optional[str]
    circulation_attribute_name: Optional[str]
    campus_id: Optional[int]

class BookResponse(BaseModel):
    """
    图书返回类
    """
    book_id: int
    title: str
    author: str|None
    publisher: str
    isbn: str|None
    multi_version_num: Optional[int]
    cover: Optional[str]
    items: List[ItemResponse]
    abstract: Optional[str]
    language_code: Optional[str]
    total_count: Optional[int]
    on_shelf_count: Optional[int]

class BookSearchResponse(BaseModel):
    """
    搜索返回类
    """
    total: int
    books: List[BookResponse]

class ItemSearchResponse(BaseModel):
    """
    条目搜索返回类
    """
    total: int
    items: List[ItemResponse]