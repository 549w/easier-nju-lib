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
    opac_collection_payload, 
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

    def get_collections(self, book_id: str) -> Dict:

        # 预请求
        pre_response = requests.post(
            OPAC_BASE_URL + OPAC_COLLECTION_API,
            json = opac_collection_payload(book_id, 1),
            headers = OPAC_HEADERS,
            verify = False
            )
        
        pre_response_dict = pre_response.json()

        self.response_check(pre_response_dict)

        total_count = pre_response_dict["data"]["totalCount"]
        
        response = requests.post(
            OPAC_BASE_URL + OPAC_COLLECTION_API,
            json = opac_collection_payload(book_id, total_count),
            headers = OPAC_HEADERS,
            verify = False
            )
        
        response_dict = response.json()
        self.response_check(response_dict)
        return response_dict
    
    def get_cover(self, isbn: str, title: str, book_id: str) -> str:
        
        response = requests.get(
            OPAC_BASE_URL + OPAC_COVER_API,
            opac_cover_payload(isbn, title, book_id),
            verify = False
            )
        
        response_dict = response.json()
        print(response_dict)

        self.response_check(response_dict)

        return response_dict["data"]