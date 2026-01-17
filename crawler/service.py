from typing import List
from crawler.models import Collection, Book, BookList, Record
from crawler.parser import NJULibParser
from crawler.client import NJULibClient
class NJULibService:
    def search(self, keyword: str, num: int) -> BookList:
        brief_html: str = NJULibClient().search(keyword, rows=num)
        brief_book_list: BookList = NJULibParser().brief_parser(brief_html)
        detailed_book_list: BookList = BookList()
        for book in brief_book_list.list:
            detail_html = NJULibClient().fetch_book_detail(book.detail_url)
            book.collection = NJULibParser().detail_parser(detail_html)
            detailed_book_list.add_book(book, merge = True)
        return detailed_book_list

    def sort_by_campus(self, book_list: BookList, campus: str) -> BookList:
        for book in book_list.list[::-1]:
            if book.in_campus(campus):
                book_list.list.remove(book)
                for record in book.collection.list:
                    if record.in_campus(campus):
                        book.collection.list.remove(record)
                        book.collection.list.insert(0, record)
                book_list.list.insert(0, book)
        return book_list