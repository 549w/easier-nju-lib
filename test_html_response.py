import requests
import sys

# 获取命令行参数作为搜索关键词
if len(sys.argv) < 2:
    print("用法: python test_html_response.py <搜索关键词>")
    sys.exit(1)

search_keyword = sys.argv[1]

# 构造请求
BASE_URL = "http://weixin.libstar.cn/weixin/unify/search"
params = {
    'searchFieldContent': search_keyword,
    'mappingPath': 'njulib',
    'groupCode': '200027',
    'searchField': 'keyWord',
    'page': 1,
    'rows': 10
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2'
}

print(f"发送请求到: {BASE_URL}")
print(f"参数: {params}")

response = requests.get(BASE_URL, params=params, headers=headers, verify=False)
print(f"\n响应状态码: {response.status_code}")
print(f"响应内容类型: {response.headers.get('Content-Type')}")

# 保存HTML内容到文件
with open(f"html_response_{search_keyword}.html", "w", encoding="utf-8") as f:
    f.write(response.text)

print(f"\nHTML响应已保存到: html_response_{search_keyword}.html")
print(f"响应长度: {len(response.text)} 字符")

# 打印前1000个字符查看
print(f"\n前1000个字符:")
print(response.text[:1000])
