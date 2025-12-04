import requests
import json

# 测试搜索API
response = requests.get('http://localhost:5000/api/search?query=python')
print(f'Status: {response.status_code}')
if response.status_code == 200:
    data = response.json()
    print(f'Found {len(data)} books')
    if data:
        print(f'First book: {data[0]["title"]}')
        if data[0].get('holdings'):
            print(f'First holding location: {data[0]["holdings"][0]["location"]}')

# 测试搜索历史API（需要有效的token）
# 请替换为实际的有效token
token = ''
if token:
    response = requests.get('http://localhost:5000/api/search-history', headers={'Authorization': f'Bearer {token}'})
    print(f'\nSearch history status: {response.status_code}')
    if response.status_code == 200:
        history = response.json()
        print(f'Search history count: {len(history)}')
        for item in history:
            print(f'  {item["query"]} - {item["search_time"]}')
