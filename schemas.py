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
    oper: Oper | None
    searchField: SearchField
    matchMode: MatchMode
    searchFieldContent: str

class SemanticFrameModel(BaseModel):
    campusId: List[CampusID | None]
    searchItems: List[SearchItemModel]

    @model_validator(mode="after")
    def check_rule(self):
        if not self.searchItems:
            raise ValueError("searchItems 不能为空")

        if self.searchItems[0].oper is not None:
            raise ValueError("第一个 oper 必须为 None")

        for i in range(1, len(self.searchItems)):
            if self.searchItems[i].oper is None:
                raise ValueError(f"第{i}个 oper 不能为 None")
            
        for i, item in enumerate(self.searchItems):
            if self.searchItems[i].searchFieldContent is None or self.searchItems[i].searchFieldContent.strip() == "":
                print("=============")
                raise ValueError(f"第{i}个 searchFieldContent 不能为空")

        return self

class ItemResponse(BaseModel):
    """
    条目返回类
    """
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
    """
    图书返回类
    """
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