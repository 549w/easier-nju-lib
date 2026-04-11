"""
crawler.service

封装上层代码直接使用的功能。
"""

from crawler.models import Collection, Book, BookList, Record
from crawler.parser import WeixinParser
from crawler.client import WeixinClient
class NJULibService:
    """
    表示抽象的图书馆服务概念。
    """
    def weixin_search(self, 
                      keyword: str, 
                      num: int, 
                      sort: bool = False, 
                      campus: str = 'default') -> BookList:
        """
        根据关键词搜索图书信息，限制最大条数。

        :param keyword: 用户输入的搜索关键词
        :param num: 最大源数据条数，指原网页上的图书条数
        :return: 包含搜索结果的 BookList 对象
        """
        brief_html: str = WeixinClient().brief_search(keyword, rows=num)
        brief_book_list: BookList = WeixinParser().brief_parser(brief_html)
        detailed_book_list: BookList = BookList()
        for book in brief_book_list.list:
            detail_html = WeixinClient().detail_search(book.detail_url)
            book.collection = WeixinParser().detail_parser(detail_html)
            detailed_book_list.add_book(book, merge = True)
        if sort:
            #print(campus)
            for book in detailed_book_list.list[::-1]:
                if book.in_campus(campus):
                    #print(f"found book {book.title} in campus {campus}")
                    detailed_book_list.list.remove(book)

                    # 当且仅当 Book 对象包含相应校区的馆藏记录时，再将其中的记录按照校区排序。
                    for record in book.collection.list:
                        if record.in_campus(campus):
                            book.collection.list.remove(record)
                            book.collection.list.insert(0, record)

                    detailed_book_list.list.insert(0, book)
        return detailed_book_list

    