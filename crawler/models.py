from config.settings import NAMES_TO_CAMPUSES
from typing import List, Dict

class Copy:
    def __init__(self, borrow_status: str, book_status: str, call_num: str, code_num: str, edition: str):
        self.borrow_status: str = borrow_status
        self.book_status: str = book_status
        self.call_num: str = call_num
        self.code_num: str = code_num
        self.edition: str = edition

class Record:
    def __init__(self, location: str):
        self.location: str | None = location
        self.campus: str | None = None
        self.copies: List[Copy] = []
        self.copy_num: int = 0
        if location[5:7] in NAMES_TO_CAMPUSES.keys():
            self.campus = NAMES_TO_CAMPUSES[location[5:7]]
    def sort_copies(self):
        self.copies.sort(key=lambda x: (x.code_num, x.call_num, x.edition))
    def add_copy(self, borrow_status: str, book_status: str, call_num: str, code_num: str, edition: str):
        new_copy: Copy = Copy(borrow_status, book_status, call_num, code_num, edition)
        self.copies.append(new_copy)
        self.copy_num += 1
        #self.sort_copies()
    def merge_copies(self, new_copies: List[Copy]):
        self.copies += new_copies
        self.copy_num += len(new_copies)
        #self.sort_copies()
    def in_campus(self, campus: str) -> bool:
        if self.campus == campus:
            return True
        return False

class Collection():
    def __init__(self):
        self.list = []
    def add_record(self, new_record: Record) -> None:
        for record in self.list:
            if record.location == new_record.location:
                record.merge_copies(new_record.copies)
                return None
        self.list.append(new_record)
        return None


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
    def in_campus(self, campus: str) -> bool:
        for record in self.collection.list:
            if record.in_campus(campus):
                return True
        return False

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
    def in_campus(self, campus: str) -> bool:
        for book in self.list:
            if book.in_campus(campus):
                return True
        return False
    def sort_by_press(self, press: str):
        for book in self.list[::-1]:
            if press in book.publication_info:
                self.list.remove(book)
                self.list.insert(0, book)
        return self