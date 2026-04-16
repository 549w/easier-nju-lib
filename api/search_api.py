from fastapi import (
    APIRouter, 
    HTTPException, 
    Response,
    Request
    )
from pydantic import BaseModel

from service.search_service import (
    intent_phrase_to_semantic_frame,
    semantic_frame_to_query,
    book_search,
    item_search
)
from schemas import (
    SemanticFrameModel,
    BookSearchResponse,
    ItemSearchResponse
)
from crawler.payloads import AdvancedSearchQuery
from exceptions import LLMError
from utils.identity import get_or_set_anon_id
import logging
import datetime
import json

router = APIRouter(prefix="/search", tags=["search"])
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(message)s'
)
logger = logging.getLogger(__name__)

class SearchBookRequest(BaseModel):
    intent_phrase: str
    page: int = 1
    rows: int = 10


class NLSearchResponse(BaseModel):
    query: AdvancedSearchQuery
    result: BookSearchResponse


@router.post("/books/llm_query", response_model=NLSearchResponse)
async def search_books_llm_query(
    request_body: SearchBookRequest,
    request: Request,
    response: Response
    ):
    """自然语言搜索书籍"""
    # 验证搜索词长度不超过50字
    if len(request_body.intent_phrase.strip()) > 50:
        raise HTTPException(
            status_code=400,
            detail={
                "code": "TOO_LONG",
                "message": "搜索意图不能多于五十个字。"
            }
        )

    try:
        semantic_frame: SemanticFrameModel = intent_phrase_to_semantic_frame(
            request_body.intent_phrase.strip()
        )
    except LLMError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    query = semantic_frame_to_query(semantic_frame, request_body.page, request_body.rows)
    search_result = book_search(query)
    anon_id = get_or_set_anon_id(request, response)
    log_data = {
        "anon_id": anon_id,
        "time": datetime.datetime.now().isoformat(),
        "user_prompt": request_body.intent_phrase,
        }
    logger.info(json.dumps(log_data, indent=4, ensure_ascii=False))
    return NLSearchResponse(query=query, result=search_result)


@router.post("/books/normal_query", response_model=BookSearchResponse)
async def search_books_normal_query(query: AdvancedSearchQuery):
    """普通搜索书籍"""
    return book_search(query)


@router.get("/items/{book_id}", response_model=ItemSearchResponse)
async def search_items(
    book_id: str,
    page: int = 1,
    rows: int = 10,
    sort_type: int = 0
):
    """搜索书籍的馆藏明细"""
    return item_search(book_id, page, rows, sort_type)
