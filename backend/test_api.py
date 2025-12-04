import requests

# 测试搜索API
def test_search_api():
    url = 'http://127.0.0.1:5000/search'
    params = {'query': 'python'}
    
    try:
        response = requests.get(url, params=params)
        print(f"状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")
        print(f"响应内容: {response.json()}")
    except Exception as e:
        print(f"请求失败: {e}")

if __name__ == '__main__':
    test_search_api()