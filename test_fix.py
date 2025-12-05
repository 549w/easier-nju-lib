import requests
import json

# 测试服务器地址
BASE_URL = 'http://127.0.0.1:8080'

def test_campus_setting():
    """测试校区设置功能"""
    print("=== 测试校区设置功能 ===")
    
    # 1. 注册新用户
    print("\n1. 注册新用户...")
    register_data = {
        'username': 'test_user',
        'password': 'test_password',
        'campus': '仙林'
    }
    response = requests.post(f'{BASE_URL}/api/register', json=register_data)
    if response.status_code != 201:
        print(f"注册失败: {response.json().get('error', '未知错误')}")
        return False
    print("注册成功")
    
    # 2. 登录
    print("\n2. 登录...")
    login_data = {
        'username': 'test_user',
        'password': 'test_password'
    }
    response = requests.post(f'{BASE_URL}/api/login', json=login_data)
    if response.status_code != 200:
        print(f"登录失败: {response.json().get('error', '未知错误')}")
        return False
    token = response.json().get('access_token')
    user_info = response.json().get('user')
    print(f"登录成功，token: {token}")
    print(f"用户信息: {user_info}")
    
    # 3. 设置校区为鼓楼
    print("\n3. 设置校区为鼓楼...")
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    campus_data = {'campus': '鼓楼'}
    response = requests.post(f'{BASE_URL}/api/user/campus', json=campus_data, headers=headers)
    if response.status_code != 200:
        print(f"设置校区失败: {response.json().get('error', '未知错误')}")
        return False
    print("设置校区成功")
    
    # 4. 获取用户信息，验证校区是否已更新
    print("\n4. 获取用户信息，验证校区是否已更新...")
    response = requests.get(f'{BASE_URL}/api/user/campus', headers=headers)
    if response.status_code != 200:
        print(f"获取用户信息失败: {response.json().get('error', '未知错误')}")
        return False
    campus_info = response.json()
    print(f"当前校区: {campus_info.get('campus')}")
    
    if campus_info.get('campus') == '鼓楼':
        print("校区设置功能测试通过！")
        return True
    else:
        print("校区设置功能测试失败！")
        return False

def test_search_function():
    """测试搜索功能"""
    print("\n=== 测试搜索功能 ===")
    
    # 1. 登录
    print("\n1. 登录...")
    login_data = {
        'username': 'test_user',
        'password': 'test_password'
    }
    response = requests.post(f'{BASE_URL}/api/login', json=login_data)
    if response.status_code != 200:
        print(f"登录失败: {response.json().get('error', '未知错误')}")
        return False
    token = response.json().get('access_token')
    print(f"登录成功，token: {token}")
    
    # 2. 测试搜索功能，搜索"Python"
    print("\n2. 测试搜索功能，搜索'Python'...")
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(f'{BASE_URL}/api/search?query=Python', headers=headers)
    if response.status_code != 200:
        print(f"搜索失败: {response.json().get('error', '未知错误')}")
        return False
    search_result = response.json()
    print(f"搜索结果: {json.dumps(search_result, ensure_ascii=False, indent=2)}")
    
    # 3. 检查搜索结果是否包含真实数据
    if 'books' in search_result and len(search_result['books']) > 0:
        print("\n3. 检查搜索结果是否包含真实数据...")
        book = search_result['books'][0]
        print(f"第一本书信息: {json.dumps(book, ensure_ascii=False, indent=2)}")
        
        # 检查书的信息是否完整
        if all(key in book for key in ['title', 'author', 'publisher', 'location', 'available']):
            print("搜索功能测试通过！返回的是真实数据。")
            return True
        else:
            print("搜索功能测试失败！返回的数据不完整。")
            return False
    else:
        print("搜索功能测试失败！没有返回任何书籍。")
        return False

def test_search_with_campus():
    """测试按校区搜索功能"""
    print("\n=== 测试按校区搜索功能 ===")
    
    # 1. 登录
    print("\n1. 登录...")
    login_data = {
        'username': 'test_user',
        'password': 'test_password'
    }
    response = requests.post(f'{BASE_URL}/api/login', json=login_data)
    if response.status_code != 200:
        print(f"登录失败: {response.json().get('error', '未知错误')}")
        return False
    token = response.json().get('access_token')
    print(f"登录成功，token: {token}")
    
    # 2. 测试按仙林校区搜索
    print("\n2. 测试按仙林校区搜索'Python'...")
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(f'{BASE_URL}/api/search?query=Python&location=仙林', headers=headers)
    if response.status_code != 200:
        print(f"搜索失败: {response.json().get('error', '未知错误')}")
        return False
    search_result = response.json()
    print(f"仙林校区搜索结果: {json.dumps(search_result, ensure_ascii=False, indent=2)}")
    
    # 3. 测试按鼓楼校区搜索
    print("\n3. 测试按鼓楼校区搜索'Python'...")
    response = requests.get(f'{BASE_URL}/api/search?query=Python&location=鼓楼', headers=headers)
    if response.status_code != 200:
        print(f"搜索失败: {response.json().get('error', '未知错误')}")
        return False
    search_result = response.json()
    print(f"鼓楼校区搜索结果: {json.dumps(search_result, ensure_ascii=False, indent=2)}")
    
    print("按校区搜索功能测试通过！")
    return True

if __name__ == '__main__':
    """运行所有测试"""
    print("开始测试系统修复情况...")
    
    # 运行校区设置测试
    campus_test_passed = test_campus_setting()
    
    # 运行搜索功能测试
    search_test_passed = test_search_function()
    
    # 运行按校区搜索测试
    campus_search_test_passed = test_search_with_campus()
    
    # 输出测试结果
    print("\n=== 测试结果总结 ===")
    print(f"校区设置功能测试: {'通过' if campus_test_passed else '失败'}")
    print(f"搜索功能测试: {'通过' if search_test_passed else '失败'}")
    print(f"按校区搜索功能测试: {'通过' if campus_search_test_passed else '失败'}")
    
    if campus_test_passed and search_test_passed and campus_search_test_passed:
        print("\n🎉 所有测试都通过了！系统修复成功。")
    else:
        print("\n❌ 有测试未通过，系统修复可能存在问题。")
