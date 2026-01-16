import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config.settings import NAMES_TO_CAMPUSES
from typing import List, Dict


class Collection():
    def __init__(self):
        self.list = []
    def add_record(self, location: str, borrow_status: str, book_status: str, call_num: str, code_num: str) -> None:
        record = {
            'location': location,
            'borrow_status': borrow_status,
            'book_status': book_status,
            'call_num': call_num,
            'code_num': code_num,
            'campus': 'undefined'
        }
        if location[5:7] in NAMES_TO_CAMPUSES.keys():
            record['campus'] = NAMES_TO_CAMPUSES[location[5:7]]
        self.list.append(record)


class Book():
    def __init__(self, title: str, author: str, isbn: str, publication_info: str, detail_url: str):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.publication_info = publication_info
        self.collection = Collection()
        self.detail_url = detail_url
    def add_collection(self, new_collection: Collection) -> None:
        # TODO: add exceptions
        self.collection.list += new_collection.list

class BookList():
    def __init__(self):
        self.list: List[Book] = []
    def add_book(self, new_book: Book, merge: bool) -> bool:
        if merge:
            for book in self.list:
                if book.isbn == new_book.isbn and book.title == new_book.title:
                    book.add_collection(new_book.collection)
                    return True
        self.list.append(new_book)
        return True