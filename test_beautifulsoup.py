import requests
import sys
from bs4 import BeautifulSoup

# 从命令行获取搜索关键词
if len(sys.argv) < 2:
    print("请提供搜索关键词")
    sys.exit(1)

search_title = sys.argv[1]

# 使用与opac_spider.py相同的搜索参数
url = "http://weixin.libstar.cn/weixin/unify/search"
params = {
    'mappingPath': 'njulib',
    'groupCode': '200027',
    'openid': 'oeL7DjraEzAnkWJpPrebGqI6B55I',
    'pubId': '1',
    'searchFieldContent': search_title,
    'searchField': 'keyWord',
    'page': '1',
    'rows': '10'
}

print(f"搜索关键词: {search_title}")
print(f"请求URL: {url}")
print(f"请求参数: {params}")

# 发送请求
response = requests.get(url, params=params)
print(f"\n响应状态码: {response.status_code}")
print(f"响应内容类型: {response.headers.get('Content-Type')}")

# 保存HTML响应到文件
with open(f'html_response_{search_title}.html', 'w', encoding='utf-8') as f:
    f.write(response.text)

# 使用BeautifulSoup解析HTML
print(f"\n正在使用BeautifulSoup解析HTML...")
soup = BeautifulSoup(response.text, 'lxml')

# 测试不同的选择器
selectors_to_test = [
    'a.weui-media-box_appmsg',
    'div.weui-media-box',
    'a',
    'div'
]

for selector in selectors_to_test:
    elements = soup.select(selector)
    print(f"选择器 '{selector}' 找到 {len(elements)} 个元素")

# 如果找到了图书元素，尝试提取详细信息
if soup.select('a.weui-media-box_appmsg'):
    print("\n=== 详细解析图书信息 ===")
    for i, book_element in enumerate(soup.select('a.weui-media-box_appmsg')[:5]):
        print(f"\n图书 {i+1}:")
        print(f"元素HTML: {book_element}")
        
        # 尝试提取标题
        title_elem = book_element.select_one('h4.weui-media-box__title')
        if title_elem:
            print(f"标题: {title_elem.get_text(strip=True)}")
        
        # 尝试提取描述信息
        desc_elements = book_element.select('p.weui-media-box__desc')
        for j, desc_elem in enumerate(desc_elements):
            print(f"描述 {j+1}: {desc_elem.get_text(strip=True)}")
