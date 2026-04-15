# 啦啦啦，advanced search不用unfold!
from config.settings import (
    DASHSCOPE_API_KEY, 
    SYSTEM_PROMPT,
    MODEL_BASE_URL,
    MODEL_NAME
    )
from crawler.models import Book, Item
from crawler.client import OpacClient
from crawler.parser import OpacParser
from crawler.payloads import (
    AdvancedSearchQuery,
    AdvancedSearchQueryBuilder,
    opac_advanced_search_payload,
    )
from mappers.response_mappers import (
    book_response_mapper,
    item_response_mapper,
    book_search_response_mapper,
    item_search_response_mapper
    )
from schemas import (
    SemanticFrameModel,
    BookSearchResponse,
    ItemResponse,
    ItemSearchResponse
    )
from dataclasses import dataclass, field
from typing import List, Dict
from openai import OpenAI
import json
from exceptions import (
    QueryValidationError,
    LLMError
)

def intent_phrase_to_semantic_frame(
        intent_phrase: str
) -> SemanticFrameModel:
    client = OpenAI(
        api_key=DASHSCOPE_API_KEY,
        base_url=MODEL_BASE_URL,
        )
    completion = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {'role': 'system', 'content': SYSTEM_PROMPT},
            {'role': 'user', 'content': intent_phrase}
        ],
        temperature=0,
        response_format={
            "type": "json_object"
            },
        max_tokens=200
    )
    #print(completion.choices[0].message.content)
    #assert completion.usage is not None
    #print(completion.usage.completion_tokens)
    #print(completion.usage.prompt_tokens)
    #print(completion.choices[0].finish_reason)
    #print(completion.id)
    #print(completion.created)
    #print(completion.model)
    #print(type(completion.choices[0].message.content))
    if not completion.usage:
        raise LLMError("无使用数据")
    if completion.choices[0].finish_reason != "stop":
        raise LLMError(f"结束原因异常，为{completion.choices[0].finish_reason}")
    if not completion.choices[0].message.content:
        raise LLMError("无输出")
    completion_tokens: int = completion.usage.completion_tokens
    content: str = completion.choices[0].message.content
    content_dict: Dict = json.loads(content)
    try:
        return SemanticFrameModel(**content_dict)
    except Exception as e:
        #print("LLM输出不合法:", content)
        raise LLMError(e)

def semantic_frame_to_query(
        semantic_frame: SemanticFrameModel,
        page: int,
        rows: int,
) -> AdvancedSearchQuery:
    
    query = AdvancedSearchQueryBuilder()
    query.set_campus(semantic_frame.campusId)
    query.set_rows(rows)
    query.set_page(page)
    for item in semantic_frame.searchItems:
        query.add_search_item(
            item.oper,
            item.searchField,
            item.matchMode,
            item.searchFieldContent
            )
    return query.build()

def book_search(
        query: AdvancedSearchQuery
        ) -> BookSearchResponse:
    
    books_raw: Dict = OpacClient().advanced_search(query)
    #print("搜索完成")
    books_data: Dict = books_raw["data"]
    books_total: int = books_data["numFound"]
    book_results: List[Dict] = books_data["searchResult"]
    book_list: List[Book] = []
    #print("book_list开始构造")
    for book_dict in book_results:
        new_book: Book = OpacParser().book_parser(
            book_dict
            )
        #print("开始抓取封面")
        new_book.cover = OpacClient().get_cover(
            new_book.isbn if new_book.isbn else "",
            new_book.title if new_book.title else "",
            str(new_book.book_id) if new_book.book_id else ""
            )
        book_list.append(
            new_book
            )
        
    return book_search_response_mapper(
        books_total,
        book_list
        )

def item_search(
        book_id: str,
        page: int,
        rows: int,
        sort_type: int = 0
        ) -> ItemSearchResponse:
    item_list: List[Item] = []
    items_raw: Dict = OpacClient().get_items(
        str(book_id),
        page,
        rows,
        sort_type
        )
    items_data = items_raw.get("data")
    if not items_data:
        return item_search_response_mapper(0, [])
        
    item_total: int = items_data.get("totalCount", 0)
    item_results: List[Dict] = items_data.get("list", [])
    for item_dict in item_results:
        item_list.append(
            OpacParser().item_parser(item_dict)
            )
    return item_search_response_mapper(
        item_total,
        item_list
        )

