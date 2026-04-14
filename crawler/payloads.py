from config.magic_params import MAGIC_PARAMS
from mappers.code_mappers import MATCH_MODE_TO_CODE
from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum
from pydantic import BaseModel, model_validator

class Oper(Enum):
    AND = "AND"
    OR = "OR"

class SearchField(Enum):
    题名 = "title"
    责任者 = "author"
    出版社 = "publisher"

class MatchMode(Enum):
    完全匹配 = "1"
    任意匹配 = "2"
    前方匹配 = "3"
    后方匹配 = "4"

class CampusID(Enum):
    鼓楼校区 = 1
    仙林校区 = 2
    院系分馆 = 3
    浦口校区 = 5
    苏州校区 = 7

@dataclass
class SearchItem:
    oper: Oper|None
    searchField: SearchField
    matchMode: MatchMode
    searchFieldContent: str

class AdvancedSearchQuery(BaseModel):
    campusId: List[Optional[CampusID]] = field(default_factory=list)
    page: int = 1
    rows: int = 10
    searchItems: List[SearchItem] = field(default_factory=list)

class AdvancedSearchQueryBuilder:
    def __init__(self):
        self.query = AdvancedSearchQuery()
    
    def build(self) -> AdvancedSearchQuery:
        return self.query

    def set_page(
            self, 
            page: int
            ) -> None:
        self.query.page = page

    def set_rows(
            self, 
            rows: int
            ) -> None:
        self.query.rows = rows
    def add_search_item(
            self, 
            oper: Oper|None, 
            search_field: SearchField, 
            match_mode: MatchMode, 
            search_field_content: str
            ) -> None:
        self.query.searchItems.append(
            SearchItem(
                oper if self.query.searchItems else None,
                search_field,
                match_mode,
                search_field_content
            )
            )
    def set_campus(
            self, 
            campus_list: List[Optional[CampusID]]
            ) -> None:
        self.query.campusId.extend(campus_list)

def opac_search_payload(keyword: str, page: int = 1, rows: int = 15):
    return {
        "docCode": [
            None
        ],
        "litCode": [],
        "searchFieldContent": keyword,
        "searchField": "keyWord",
        "matchMode": "2",
        "resourceType": [],
        "subject": [],
        "discode1": [],
        "publisher": [],
        "libCode": [],
        "locationId": [],
        "eCollectionIds": [],
        "neweCollectionIds": [],
        "curLocationId": [],
        "campusId": [],
        "kindNo": [],
        "collectionName": [],
        "author": [],
        "langCode": [],
        "countryCode": [],
        "publishBegin": None,
        "publishEnd": None,
        "coreInclude": [],
        "ddType": [],
        "verifyStatus": [],
        "group": [],
        "sortField": "relevance",
        "sortClause": "asc",
        "page": page,
        "rows": rows,
        "onlyOnShelf": None,
        "searchItems": None,
        "newCoreInclude": [],
        "customSub": [],
        "customSub0": [],
        "indexSearch": 1
    }
def opac_advanced_search_payload(query: AdvancedSearchQuery):

    query_json = query.model_dump(
        mode="json"
    )
    campus_id = query_json.get("campusId", [])
    if campus_id == [None]:
        campus_id = []
    
    return {
    "docCode": [
        None
    ],
    "litCode": [],
    "matchMode": "2",
    "resourceType": [],
    "subject": [],
    "discode1": [],
    "publisher": [],
    "libCode": [],
    "locationId": [],
    "eCollectionIds": [],
    "neweCollectionIds": [],
    "curLocationId": [],
    "campusId": campus_id,
    "kindNo": [],
    "collectionName": [],
    "author": [],
    "langCode": [],
    "countryCode": [],
    "publishBegin": None,
    "publishEnd": None,
    "coreInclude": [],
    "ddType": [],
    "verifyStatus": [],
    "group": [],
    "sortField": "relevance",
    "sortClause": "asc",
    "page": query_json.get("page"),
    "rows": query_json.get("rows"),
    "onlyOnShelf": None,
    "searchItems": query_json.get("searchItems"),
    "searchFieldContent": "",
    "searchField": "keyWord",
    "searchFieldList": None,
    "isOpen": False
}

def opac_cover_payload(
        isbn: str|None, 
        title: str|None, 
        book_id: str|None
        ):

    return {
        "isbn": isbn if isbn else "",
        "title": title,
        "recordId": book_id
    }

def opac_items_payload(book_id: str, page: int, rows: int, sort_type: int = 0):
    
    return {
        "page": page,
        "rows": rows, # 这玩意应该从响应体的 totalCount 中获取
        "entrance": None,
        "recordId": book_id,
        "isUnify": True,
        "sortType": sort_type,
        "callNo": ""
    }