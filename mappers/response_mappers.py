from crawler.models import Item, Book
from schemas import (
    ItemResponse,
    BookResponse,
    BookSearchResponse,
    ItemSearchResponse
    )
from typing import List

def item_response_mapper(
        item: Item
        ) -> ItemResponse:
    
    return ItemResponse(
        item_id=int(item.item_id) if item.item_id else None,
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

def book_search_response_mapper(
        total: int,
        books: List[Book]
        ) -> BookSearchResponse:
    
    return BookSearchResponse(
        total=total,
        books=[
            book_response_mapper(book)
            for book in books
            ]
    )

def item_search_response_mapper(
        total: int,
        items: List[Item]
        ) -> ItemSearchResponse:
    
    return ItemSearchResponse(
        total=total,
        items=[
            item_response_mapper(item)
            for item in items
            ]
    )