import requests
from config.settings import BASE_URL, SEARCH_API
from config.magic_params import MAGIC_PARAMS
from exceptions import NetworkError
class NJULibClient:
    def search(self, keyword: str, page: int = 1, rows: int = 15) -> str:
        params = {
            'mappingPath': MAGIC_PARAMS['mappingPath'],
            'groupCode': MAGIC_PARAMS['groupCode'],
            'pubId': MAGIC_PARAMS['pubId'],
            'searchFieldContent': keyword,
            'searchField': MAGIC_PARAMS['searchField'],
            'page': page,
            'rows': rows
        }
        response = requests.get(BASE_URL + SEARCH_API, params)
        if response.status_code != 200:
            raise NetworkError(f'HTTP {response.status_code}')
        response.encoding = 'utf-8'
        return response.text
    def fetch_book_detail(self, detail_url: str) -> str:
        response = requests.get(BASE_URL + detail_url)
        if response.status_code != 200:
            raise NetworkError(f'HTTP {response.status_code}')
        response.encoding = 'utf-8'
        return response.text