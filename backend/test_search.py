import requests
import json

# 测试不同关键词的搜索功能
def test_search_keywords():
    keywords = ['Python', 'Java', '数学', '测试', '未知关键词']
    results = {}
    
    for keyword in keywords:
        print(f"\n测试搜索关键词: {keyword}")
        try:
            response = requests.get(f"http://localhost:5000/search?query={keyword}")
            if response.status_code == 200:
                books = response.json()
                results[keyword] = books
                print(f"搜索成功，返回 {len(books)} 本书")
                print(f"第一本书: {json.dumps(books[0], ensure_ascii=False, indent=2)}")
            else:
                print(f"搜索失败，状态码: {response.status_code}")
                print(f"错误信息: {response.text}")
        except Exception as e:
            print(f"请求出错: {str(e)}")
    
    return results

if __name__ == "__main__":
    print("开始测试后端搜索功能...")
    test_search_keywords()
    print("\n测试完成!")