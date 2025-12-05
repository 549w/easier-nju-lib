import requests
import json

# 测试API地址
BASE_URL = 'http://localhost:5000/api'

def test_search():
    """测试搜索功能"""
    print("=== 测试搜索功能 ===")
    url = f'{BASE_URL}/search'
    params = {'query': 'Python'}
    response = requests.get(url, params=params)
    print(f"状态码: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"搜索结果数量: {len(data) if isinstance(data, list) else 0}")
        
        if data and isinstance(data, list):
            # 打印第一本书的详细信息
            first_book = data[0]
            print(f"\n第一本书信息:")
            print(f"标题: {first_book.get('title')}")
            print(f"作者: {first_book.get('author')}")
            print(f"出版社: {first_book.get('publisher')}")
            print(f"年份: {first_book.get('year')}")
            
            # 打印完整的book对象结构
            print("\n完整的book对象结构:")
            print(f"所有键: {list(first_book.keys())}")
            
            # 检查馆藏信息
            if 'holdings' in first_book:
                print(f"holdings字段存在，类型: {type(first_book['holdings'])}")
                holdings = first_book['holdings']
                if isinstance(holdings, list):
                    print(f"holdings长度: {len(holdings)}")
                    if holdings:
                        print("\n馆藏信息: holdings数组格式")
                        for i, holding in enumerate(holdings):
                            print(f"  馆藏 {i+1}:")
                            print(f"    所有键: {list(holding.keys())}")
                            print(f"    索书号: {holding.get('callNumber')}")
                            print(f"    馆藏地: {holding.get('location')}")
                            print(f"    状态: {holding.get('status')}")
            else:
                print("\n馆藏信息: 直接字段格式")
                print(f"  索书号: {first_book.get('callNumber')}")
                print(f"  馆藏地: {first_book.get('location')}")
                print(f"  状态: {first_book.get('status')}")
                print(f"  是否有callNumber字段: {'callNumber' in first_book}")
                print(f"  是否有location字段: {'location' in first_book}")
                print(f"  是否有status字段: {'status' in first_book}")
    else:
        print(f"错误信息: {response.text}")

if __name__ == "__main__":
    test_search()