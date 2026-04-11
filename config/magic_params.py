"""
本项目中会使用到的各种意义不明的基础信息。
主要是原网页请求中的魔法参数。
"""

MAGIC_PARAMS = {
    'mappingPath': 'njulib',
    'groupCode': 200027, # If changed to 200026, results will change and cannot be clicked. If changed to others, there will be no results.
    'pubId': 1,
    'searchField': 'keyWord'
}

OPAC_HEADERS = {
    "Content-Type": "application/json;charset=utf-8",
    #"Accept": "application/json, text/plain, */*",
    #"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15",
    #"Referer": "https://opac.nju.edu.cn/",
    #"Cookie": "SameSite=None; _ga_VJQNNH3B5M=...; _ga=...",
    "groupCode": "200027",
    #"x-lang": "CHI",
}