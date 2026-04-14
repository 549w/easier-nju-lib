from typing import List

class Item:
    """
    一本藏书。
    """
    def __init__(
            self,
            item_id: str|None, # 系统内部id，对应源数据中的"itemId"
            call_no: str|None, # 索书号，对应"callNo"
            barcode: str|None, # 条码号，对应"barcode"
            current_location_code: int|None,
            process_type_code: int|None,
            circulation_attribute_code: str|None,
            ):
        self.item_id: str|None = item_id
        self.call_no: str|None = call_no
        self.barcode: str|None = barcode
        self.current_location_code: int|None = current_location_code # 当前馆藏地，对应源数据中的"curLocationId"
        self.process_type_code: int|None = process_type_code # 当前状态，对应"processTypeCode"
        self.circulation_attribute_code: str|None = circulation_attribute_code # 流通属性，对应"circAttr"

class Book:
    """
    一种书。
    """

    def __init__(
            self,
            book_id: int,
            title: str,
            author: str,
            publisher: str,
            isbn: str,
            multi_version_num: int|None
            ):
        self.book_id: int = book_id
        self.title: str = title
        self.author: str = author
        self.publisher: str = publisher
        self.isbn: str = isbn
        self.multi_version_num: int|None = multi_version_num
        self.cover: str|None = None
        self.items: List[Item] = []
        self.items_count: int|None = None
        self.abstract: str|None = None
        self.language_code: str|None = None