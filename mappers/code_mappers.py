"""
根据原系统中的字典构建映射表，供项目调用
"""

import json
from pprint import pprint

with open('mappers/code_dict.json', 'r', encoding='utf-8') as _f:
    _code_dict_data = json.load(_f)
with open('mappers/opac_search_field_para_list.json', 'r', encoding='utf-8') as _f:
    _para_list_data = json.load(_f)
with open('mappers/location_list.json', 'r', encoding='utf-8') as _f:
    _location_list_data = json.load(_f)

CODE_TO_CAMPUS = {}
CAMPUS_TO_CODE = {}
for _c in _code_dict_data["data"]["campusCode"]:
    CODE_TO_CAMPUS[_c["campusId"]] = _c["campusName"]
    CAMPUS_TO_CODE[_c["campusName"]] = _c["campusId"]

CODE_TO_LOCATION = {}
LOCATION_TO_CODE = {}

for _l in _code_dict_data["data"]["locationId"]:
    CODE_TO_LOCATION[_l["code"]] = _l["name"]
    LOCATION_TO_CODE[_l["name"]] = _l["code"]

LOCATION_ID_TO_CAMPUS_ID = {}
for _l in _location_list_data["data"]["donateList"]:
    LOCATION_ID_TO_CAMPUS_ID[_l["locationId"]] = _l["campusId"]

CODE_TO_COUNTRY = {}
COUNTRY_TO_CODE = {}

for _l in _code_dict_data["data"]["countryCode"]:
    CODE_TO_COUNTRY[_l["code"]] = _l["name"]
    COUNTRY_TO_CODE[_l["name"]] = _l["code"]

PROCESS_TYPE_TO_CODE = {}
CODE_TO_PROCESS_TYPE = {}
for _l in _code_dict_data["data"]["processTypeList"]:
    PROCESS_TYPE_TO_CODE[_l["name"]] = _l["code"]
    CODE_TO_PROCESS_TYPE[_l["code"]] = _l["name"]

CIRCULATION_TYPE_TO_CODE = {}
CODE_TO_CIRCULATION_TYPE = {}
for _l in _code_dict_data["data"]["circAttr"]:
    CIRCULATION_TYPE_TO_CODE[_l["name"]] = _l["code"]
    CODE_TO_CIRCULATION_TYPE[_l["code"]] = _l["name"]

MATCH_MODE_TO_CODE = {
    "完全匹配": "1",
    "任意匹配": "2",
    "前方匹配": "3",
    "后方匹配": "4"  
}
CODE_TO_MATCH_MODE = {
    v: k for k, v in MATCH_MODE_TO_CODE.items()
    }

SEARCH_FIELD_TO_CODE = {}
CODE_TO_SEARCH_FIELD = {}
for _l in _para_list_data["data"]:
    SEARCH_FIELD_TO_CODE[_l["searchField"]] = _l["id"]
    CODE_TO_SEARCH_FIELD[_l["id"]] = _l["searchField"]

SORT_TYPE_TO_CODE = {
    "按索书号升序": "1",
    "按索书号降序": "2",
    "按馆藏地升序": "3",
    "按馆藏地降序": "4",
    "按馆藏地升序": "5",
    "按馆藏地降序": "6",
    "按馆藏地升序": "7",
    "按馆藏地降序": "8",
}