from typing import List
from models import Collection, Book, BookList
from parser import NJULibParser
from client import NJULibClient
class NJULibService:
    def search(self, keyword: str) -> BookList:
        brief_html: str = NJULibClient().search(keyword)
        brief_book_list: BookList = NJULibParser().brief_parser(brief_html)
        detailed_book_list: BookList = BookList()
        for book in brief_book_list.list:
            detail_html = NJULibClient().fetch_book_detail(book.detail_url)
            book.collection = NJULibParser().detail_parser(detail_html)
            detailed_book_list.add_book(book, merge = True)
        return detailed_book_list