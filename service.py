# 啦啦啦，advanced search不用unfold!
from config.settings import (
    DASHSCOPE_API_KEY, 
    SYSTEM_PROMPT,
    MODEL_BASE_URL,
    MODEL_NAME
    )
from crawler.models import Book, Item
from crawler.parser import OpacParser
from crawler.payloads import (
    opac_advanced_search_payload,
    SearchItem,
    CampusID
    )
from mappers.response_mappers import (
    book_response_mapper,
    item_response_mapper,
    search_response_mapper,
    SearchResponse
    )
from dataclasses import dataclass, field
from typing import List, Dict
from openai import OpenAI

@dataclass
class SemanticFrame:
    campusId: List[CampusID] = field(default_factory=list)
    searchItems: List[SearchItem] = field(default_factory=list)

def intent_phrase_to_semantic_frame(
        intent_phrase: str
) :
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

#def search(
#        intent_phrase: str
#) -> SearchResponse:
    