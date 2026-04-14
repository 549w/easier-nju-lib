"""
crawler.client

封装获取源数据功能，包括 html 和 json 。
"""

from typing import Dict
import requests
import json
import urllib3
from config.endpoints import *
from config.magic_params import (
    MAGIC_PARAMS, 
    OPAC_HEADERS
    )
from exceptions import NetworkError

from crawler.payloads import (
    opac_search_payload, 
    opac_advanced_search_payload, 
    opac_items_payload, 
    opac_cover_payload,
    Oper,
    SearchField,
    MatchMode,
    CampusID,
    AdvancedSearchQueryBuilder,
    AdvancedSearchQuery
)

class OpacClient:
    """
    OpacClient 类用于抓取和操作 OPAC 网站。
    """
    def __init__(self):
        urllib3.disable_warnings()
    def response_check(self, response_dict: Dict) -> None:
        """
        检查 OPAC HTTP 响应标识，并抛出异常。
        :param response: 响应体
        :return: None
        """
        if not response_dict['success']:
            raise NetworkError(f'OPAC brief search failed.')
    def brief_search(self, keyword: str, num: int = 15) -> Dict:
        
        response = requests.post(
            OPAC_BASE_URL + OPAC_SEARCH_API,
            json = opac_search_payload(keyword, num),
            headers = OPAC_HEADERS,
            verify = False)
        response_dict = response.json()

        self.response_check(response_dict)
        return response.json()
    
    def advanced_search(
            self,
            query: AdvancedSearchQuery
            ) -> Dict:
        
        response = requests.post(
            OPAC_BASE_URL + OPAC_ADVANCED_SEARCH_API,
            json = opac_advanced_search_payload(query),
            headers = OPAC_HEADERS,
            verify = False
            )
        response_dict = response.json()

        self.response_check(response_dict)
        return response.json()
    
    def get_items_count(
            self,
            book_id: str
    ) -> int:
        """
        获取书目项数量。
        :param book_id: 书目项 id
        :return: 书目项数量
        """
        response = requests.post(
            OPAC_BASE_URL + OPAC_COLLECTION_API,
            json = opac_items_payload(book_id, 1, 1),
            headers = OPAC_HEADERS,
            verify = False
            )
        
        response_dict = response.json()

        self.response_check(response_dict)
        return response_dict["data"]["totalCount"]
    def get_items(
            self, 
            book_id: str, 
            page: int = 1, 
            rows: int = 15, 
            sort_type: int = 0
            ) -> Dict:
        
        response = requests.post(
            OPAC_BASE_URL + OPAC_COLLECTION_API,
            json = opac_items_payload(book_id, 1, rows, sort_type),
            headers = OPAC_HEADERS,
            verify = False
            )
        
        response_dict = response.json()
        self.response_check(response_dict)
        return response_dict
    
    def get_cover(
            self, 
            isbn: str|None, 
            title: str|None, 
            book_id: str|None
            ) -> str:
        
        response = requests.get(
            OPAC_BASE_URL + OPAC_COVER_API,
            opac_cover_payload(isbn, title, book_id),
            verify = False
            )
        
        response_dict = response.json()
        #print(response_dict)

        self.response_check(response_dict)

        return response_dict["data"]