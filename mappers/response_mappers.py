from crawler.models import Item, Book
from schemas import (
    ItemResponse,
    BookResponse,
    SearchResponse
    )
from typing import List

def item_response_mapper(
        item: Item
        ) -> ItemResponse:
    
    return ItemResponse(
        item_id=item.item_id,
        call_no=item.call_no,
        barcode=item.barcode,
        current_location_code
        =item.current_location_code,
        process_type_code
        =item.process_type_code,
        circulation_attribute_code
        =item.circulation_attribute_code
        )

def book_response_mapper(
        book: Book
        ) -> BookResponse:
    
    return BookResponse(
        book_id=book.book_id,
        title=book.title,
        author=book.author,
        publisher=book.publisher,
        isbn=book.isbn,
        multi_version_num
        =book.multi_version_num,
        cover=book.cover,
        abstract=book.abstract,
        items=[
            item_response_mapper(item) 
            for item in book.items
            ],
        language_code=book.language_code
    )

def search_response_mapper(
        total: int,
        books: List[Book]
        ) -> SearchResponse:
    
    return SearchResponse(
        total=total,
        books=[
            book_response_mapper(book)
            for book in books
            ]
    )