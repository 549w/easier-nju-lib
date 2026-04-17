from fastapi import (
    APIRouter, 
    HTTPException, 
    Response,
    Request
    )
from pydantic import BaseModel
from db.connection import get_connection
from repository.usage_log_repo import (
    create_usage_log,
    get_usage_count,
    get_usage_logs,
    find_completion_by_prompt
    )
from service.search_service import (
    intent_phrase_to_semantic_frame,
    semantic_frame_to_query,
    book_search,
    item_search
)
from schemas import (
    SemanticFrameModel,
    BookSearchResponse,
    ItemSearchResponse,
    LLMMetadataModel
)
from crawler.payloads import AdvancedSearchQuery
from exceptions import LLMError
from utils.get_ip import get_client_ip
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
    anon_id = get_or_set_anon_id(request, response)
    ip = get_client_ip(request)
    log_data = {
        "anon_id": anon_id,
        "ip": ip,
        "time": datetime.datetime.now().isoformat(),
        "user_prompt": request_body.intent_phrase,
        }
    logger.info(json.dumps(log_data, indent=4, ensure_ascii=False))
    # 验证搜索词长度不超过50字
    if len(request_body.intent_phrase.strip()) > 50:
        raise HTTPException(
            status_code=400,
            detail={
                "code": "TOO_LONG",
                "message": "搜索意图不能多于五十个字。"
            }
        )
    cache: str|None = find_completion_by_prompt(
        get_connection(),
        request_body.intent_phrase
    )
    llm_metadata: LLMMetadataModel|None = None
    if cache:
        semantic_frame = SemanticFrameModel(**json.loads(cache))
    else:
        try:
            semantic_frame: SemanticFrameModel
            
            semantic_frame, llm_metadata = intent_phrase_to_semantic_frame(
                request_body.intent_phrase.strip()
            )
        except LLMError as e:
            raise HTTPException(
                status_code=400,
                detail=str(e)
            )
    create_usage_log(
        conn=get_connection(),
        anon_id=anon_id,
        ip=ip,
        user_prompt=request_body.intent_phrase,
        completion_content=semantic_frame.model_dump_json(),
        prompt_tokens=llm_metadata.prompt_tokens if llm_metadata else None,
        completion_tokens=llm_metadata.completion_tokens if llm_metadata else None,
        finish_reason=llm_metadata.finish_reason if llm_metadata else None,
        completion_id=llm_metadata.completion_id if llm_metadata else None,
        completed_at=llm_metadata.completed_at if llm_metadata else None,
        completion_model=llm_metadata.completion_model if llm_metadata else None,
        is_cache_hit= 1 if cache else 0
    )

    query = semantic_frame_to_query(semantic_frame, request_body.page, request_body.rows)
    search_result = book_search(query)
    
    
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
