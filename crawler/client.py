"""
crawler.client

封装获取源数据功能，包括 html 和 json 。
"""

from typing import Dict
import requests
import json
import urllib3
from config.endpoints import WEIXIN_BASE_URL, WEIXIN_SEARCH_API, OPAC_BASE_URL, OPAC_SEARCH_API
from config.magic_params import MAGIC_PARAMS, OPAC_HEADERS
from exceptions import NetworkError
from crawler.payloads import opac_search
from crawler.payloads import weixin_search

class WeixinClient:
    """
    表示抽象的从微信公众号服务中抓取网页原始数据的概念。
    """
    def brief_search(self, keyword: str, rows: int = 15) -> str:
        """
        在原网页上搜索关键词，
        限制页数和图书条数，
        抓取搜索结果页的整个网页备用。

        :param keyword: 用户输入的搜索关键词
        :param page: 请求中用于控制结果页数的参数。方便起见，本项目中始终设为 1
        :param rows: 请求中用于控制每页结果条数的参数。鉴于 page 始终为 1 ，该参数即最大源数据条数
        :return: 搜索结果页的整个网页 html
        """

        # 按照原网页的 url 组织参数
        params = weixin_search(keyword, rows)
        response = requests.get(WEIXIN_BASE_URL + WEIXIN_SEARCH_API, params)
        if response.status_code != 200:
            raise NetworkError(f'HTTP {response.status_code}')
        response.encoding = 'utf-8'
        return response.text

    def detail_search(self, detail_url: str) -> str:
        """
        抓取图书详情页的整个网页备用。

        :param detail_url: 图书详情页地址
        :return: 图书详情页的整个网页 html
        """
        response = requests.get(WEIXIN_BASE_URL + detail_url)
        if response.status_code != 200:
            raise NetworkError(f'HTTP {response.status_code}')
        response.encoding = 'utf-8'
        return response.text
    
class OpacClient:
    """
    OpacClient 类用于抓取和操作 OPAC 网站。
    """
    def brief_search(self, keyword: str, num: int = 15) -> Dict:
        urllib3.disable_warnings()
        response = requests.post(OPAC_BASE_URL + OPAC_SEARCH_API,
                  json = opac_search(keyword, num),
                  headers = OPAC_HEADERS,
                  verify = False)
        response_dict = response.json()

        if not response_dict['success']:
            raise NetworkError(f'OPAC brief search failed.')
        return response.json()