import requests

def test_search(query):
    """测试搜索功能"""
    print(f"=== 测试搜索关键词: {query} ===")
    try:
        response = requests.get(f'http://127.0.0.1:5000/api/search?query={query}')
        print(f"状态码: {response.status_code}")
        
        if response.status_code == 200:
            results = response.json()
            print(f"搜索结果数量: {len(results)}")
            
            if results:
                print("\n前5本书信息:")
                for i, book in enumerate(results[:5]):
                    print(f"{i+1}. {book['title']} - {book['author']}")
                    if book.get('holdings'):
                        print(f"   馆藏数量: {len(book['holdings'])}")
                        for j, holding in enumerate(book['holdings'][:2]):
                            print(f"      {j+1}. {holding['callNumber']} - {holding['location']} - {holding['status']}")
    except Exception as e:
        print(f"测试出错: {str(e)}")

# 测试不同的关键词
test_search("Java")
test_search("Python")
test_search("数据结构")
