"""
本项目中会使用到的各种有意义的基础信息。
"""
import os
from dotenv import load_dotenv

load_dotenv()

DASHSCOPE_API_KEY = os.getenv('DASHSCOPE_API_KEY')

CAMPUSES_TO_NAMES = {'gulou': '鼓楼', 'xianlin': '仙林', 'pukou': '浦口', 'suzhou': '苏州'}

NAMES_TO_CAMPUSES = {'鼓楼': 'gulou', '仙林': 'xianlin', '浦口': 'pukou', '苏州': 'suzhou'}

INSTRUCTION = ("这是一个小应用，希望帮你更方便地查找NJU图书馆的藏书。  "
               "除了书名之外，你还可以指定 **校区、作者和出版社** ，  "
               "符合你需要的信息将被 **优先** 并 :violet-badge[突出] 展示。")

SYSTEM_PROMPT = (
    '''
你是图书馆检索解析器。将自然语言转为JSON框架。必须返回至少一个searchItem。

【SearchField】
"title" | "author" | "publisher"

【MatchMode】
"1" 精确匹配（仅当用户要求精确）
"2" 模糊匹配（默认）
"3" 前缀匹配（“以…开头”）
"4" 后缀匹配（“以…结尾”）

【CampusID】
1 鼓楼（鼓楼/本部/老校区）
2 仙林
3 院系分馆（系图/院图）
5 浦口
7 苏州
未提及返回 [null]

【Oper】
searchItems[0].oper = null  
其余根据语义用AND或OR

【输出格式】
{
  "campusId": number[],
  "searchItems": [
    {
      "oper": "AND" | "OR" | null,
      "searchField": "title" | "author" | "publisher",
      "matchMode": "1" | "2" | "3" | "4",
      "searchFieldContent": string
    }
  ]
}
'''
)

MODEL_NAME = "qwen-plus"

MODEL_BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1"