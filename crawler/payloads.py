from config.magic_params import MAGIC_PARAMS
from mappers.code_mappers import MATCH_MODE_TO_CODE
from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum

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

@dataclass
class AdvancedSearchQuery:
    campusId: List[CampusID] = field(default_factory=list)
    page: int = 1
    rows: int = 10
    searchItems: List[SearchItem] = field(default_factory=list)

class AdvancedSearchQueryBuilder:
    def __init__(self):
        self.query = AdvancedSearchQuery()
    
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
            campus_list: List[CampusID]
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
    "campusId": query.campusId,
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
    "page": query.page,
    "rows": query.rows,
    "onlyOnShelf": None,
    "searchItems": query.searchItems,
    "searchFieldContent": "",
    "searchField": "keyWord",
    "searchFieldList": None,
    "isOpen": False
}

def opac_cover_payload(isbn: str, title: str, book_id: str):

    return {
        "isbn": isbn,
        "title": title,
        "recordId": book_id
    }

def opac_collection_payload(book_id: str, num: int):
    
    return {
        "page": 1,
        "rows": num, # 这玩意应该从响应体的 totalCount 中获取
        "entrance": None,
        "recordId": book_id,
        "isUnify": True,
        "sortType": 0,
        "callNo": ""
    }