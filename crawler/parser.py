from crawler.models import (
    Book, 
    Item
    )

class OpacParser:

    def item_parser(
            self, 
            item_dict: dict
            ) -> Item:
        new_item: Item = Item(
            item_id=item_dict.get("itemId"),
            call_no=item_dict.get("callNo"),
            barcode=item_dict.get("barcode"),
            current_location_code=item_dict.get("curLocationId"),
            process_type_code=item_dict.get("processTypeCode"),
            circulation_attribute_code=item_dict.get("circAttr")
            )
        
        return new_item
    
    def book_parser(
            self, 
            book_dict: dict
            ) -> Book:
        
        new_book = Book(
            book_id=book_dict["recordId"],
            title=book_dict["title"],
            author=book_dict["author"],
            publisher=book_dict["publisher"],
            isbn=book_dict["isbn"],
            multi_version_num=book_dict.get("multiVersionNum")
            )
        
        new_book.abstract = book_dict.get("abstract")
        new_book.language_code = book_dict.get("languageCode")

        return new_book