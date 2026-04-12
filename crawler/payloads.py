from config.magic_params import MAGIC_PARAMS

def weixin_search(keyword: str, num: int = 15):
    return {
        'mappingPath': MAGIC_PARAMS['mappingPath'],
        'groupCode': MAGIC_PARAMS['groupCode'],
        'pubId': MAGIC_PARAMS['pubId'],
        'searchFieldContent': keyword,
        'searchField': MAGIC_PARAMS['searchField'],
        'page': 1,
        'rows': num
    }
def opac_search(keyword: str, num: int = 15):
    return {
        "docCode": [
            None
        ],
        "litCode": [],
        "searchFieldContent": keyword,
        "searchField": "keyWord",
        "matchMode": "2",
        "resourceType": [],
        "subject": [],
        "discode1": [],
        "publisher": [],
        "libCode": [],
        "locationId": [],
        "eCollectionIds": [],
        "neweCollectionIds": [],
        "curLocationId": [],
        "campusId": [],
        "kindNo": [],
        "collectionName": [],
        "author": [],
        "langCode": [],
        "countryCode": [],
        "publishBegin": None,
        "publishEnd": None,
        "coreInclude": [],
        "ddType": [],
        "verifyStatus": [],
        "group": [],
        "sortField": "relevance",
        "sortClause": "asc",
        "page": 1,
        "rows": num,
        "onlyOnShelf": None,
        "searchItems": None,
        "newCoreInclude": [],
        "customSub": [],
        "customSub0": [],
        "indexSearch": 1
    }

def opac_advanced_search(keyword: str, author: str):

    return {
        "docCode":["1","2"],
            "litCode":[],
            "matchMode":"2",
            "resourceType":["1","2"],
            "subject":[],
            "discode1":[],
            "publisher":[],
            "libCode":[],
            "locationId":[90,159],
            "eCollectionIds":[],
            "neweCollectionIds":[],
            "curLocationId":[],
            "campusId":[1,2],
            "kindNo":[],
            "collectionName":[],
            "author":[],
            "langCode":["999","chi","eng"],
            "countryCode":["US","AO","CN"],
            "publishBegin":None,
            "publishEnd":None,
            "coreInclude":[],
            "ddType":[],
            "verifyStatus":[],
            "group":[],
            "sortField":"relevance",
            "sortClause":"asc",
            "page":1,
            "rows":10,
            "onlyOnShelf":None,
            "searchItems":[
                {"oper":None,
                 "searchField":"title",
                 "matchMode":"2",
                 "searchFieldContent":"一九八四"},
                 {"oper":"AND",
                  "searchField":"author",
                  "matchMode":"1",
                  "searchFieldContent":"乔治"},
                  {"oper":"OR",
                   "searchField":"isbn",
                   "matchMode":"1",
                   "searchFieldContent":"114514"}],
            "searchFieldContent":"",
            "searchField":"keyWord",
            "searchFieldList":None,
            "isOpen":False
    }

def opac_cover(isbn: str, title: str, book_id: str):

    return {
        "isbn": isbn,
        "title": title,
        "recordId": book_id
    }

def opac_collection(book_id: str, num: int):
    
    return {
        "page": 1,
        "rows": num, # 这玩意应该从响应体的 totalCount 中获取
        "entrance": None,
        "recordId": book_id,
        "isUnify": True,
        "sortType": 0,
        "callNo": ""
    }