#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试脚本：验证搜索历史记录和校区排序功能
"""
import requests
import json
import time

# API配置
BASE_URL = "http://localhost:5000"
REGISTER_URL = f"{BASE_URL}/api/register"
LOGIN_URL = f"{BASE_URL}/api/login"
SEARCH_URL = f"{BASE_URL}/api/search"
SEARCH_HISTORY_URL = f"{BASE_URL}/api/search-history"

# 测试用户信息（使用新的测试用户）
TEST_USER = {
    "username": f"test_user_{int(time.time())}",
    "password": "test123",
    "campus": "鼓楼"
}

def test_search_history():
    """测试搜索历史记录功能"""
    print("=== 测试搜索历史记录功能 ===")
    
    # 1. 注册新用户
    print("\n1. 注册新用户...")
    response = requests.post(REGISTER_URL, json=TEST_USER)
    if response.status_code != 201:
        print(f"注册失败: {response.status_code} - {response.text}")
        return False
    print(f"注册成功: {TEST_USER['username']}")
    
    # 2. 登录获取token
    print("\n2. 登录测试用户...")
    login_data = {"username": TEST_USER["username"], "password": TEST_USER["password"]}
    response = requests.post(LOGIN_URL, json=login_data)
    if response.status_code != 200:
        print(f"登录失败: {response.status_code} - {response.text}")
        return False
    
    login_data = response.json()
    token = login_data.get("access_token")
    if not token:
        print("获取token失败")
        return False
    print(f"登录成功，获取到token")
    
    # 3. 设置请求头（包含token）
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    # 4. 执行搜索
    print("\n3. 执行搜索...")
    test_query = f"测试搜索历史_{int(time.time())}"
    response = requests.get(SEARCH_URL, params={"query": test_query}, headers=headers)
    if response.status_code != 200:
        print(f"搜索失败: {response.status_code} - {response.text}")
        return False
    print(f"搜索成功，查询关键词: {test_query}")
    
    # 5. 获取搜索历史
    print("\n4. 获取搜索历史...")
    response = requests.get(SEARCH_HISTORY_URL, headers=headers)
    if response.status_code != 200:
        print(f"获取搜索历史失败: {response.status_code} - {response.text}")
        return False
    
    search_history = response.json()
    print(f"获取到 {len(search_history)} 条搜索历史记录")
    for record in search_history:
        print(f"  - {record.get('query')} ({record.get('search_time')})")
    
    # 6. 验证搜索历史是否包含刚刚执行的搜索
    if any(record.get('query') == test_query for record in search_history):
        print(f"\n✅ 验证成功：搜索历史中包含刚刚执行的搜索 '{test_query}'")
        return True
    else:
        print(f"\n❌ 验证失败：搜索历史中不包含刚刚执行的搜索 '{test_query}'")
        return False

def test_campus_sorting():
    """测试校区排序功能"""
    print("\n=== 测试校区排序功能 ===")
    
    # 1. 登录测试用户（鼓楼校区）
    print("\n1. 登录鼓楼校区测试用户...")
    login_data = {"username": TEST_USER["username"], "password": TEST_USER["password"]}
    response = requests.post(LOGIN_URL, json=login_data)
    if response.status_code != 200:
        print(f"登录失败: {response.status_code} - {response.text}")
        return False
    
    login_data = response.json()
    token = login_data.get("access_token")
    if not token:
        print("获取token失败")
        return False
    print(f"登录成功，用户校区：{TEST_USER['campus']}")
    
    # 2. 设置请求头（包含token）
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    # 3. 执行搜索
    print("\n2. 执行搜索...")
    response = requests.get(SEARCH_URL, params={"query": "python"}, headers=headers)
    if response.status_code != 200:
        print(f"搜索失败: {response.status_code} - {response.text}")
        return False
    
    books = response.json()
    print(f"搜索成功，返回 {len(books)} 本图书")
    
    # 4. 验证校区排序
    print("\n3. 验证校区排序...")
    if not books:
        print("没有找到图书，无法验证校区排序")
        return True
    
    for i, book in enumerate(books[:3]):  # 只检查前3本图书
        print(f"\n图书 {i+1}: {book.get('title')}")
        if not book.get('holdings'):
            print("  无馆藏信息")
            continue
        
        # 检查第一馆藏是否为鼓楼校区
        first_holding = book['holdings'][0]
        location = first_holding.get('location', '')
        print(f"  第一馆藏地: {location}")
        print(f"  馆藏列表:")
        for j, holding in enumerate(book['holdings']):
            print(f"    {j+1}. {location}: {holding.get('status', '')}")
        
        # 验证第一馆藏是否为鼓楼校区
        if "鼓楼" in location:
            print(f"    ✅ 第一馆藏地为鼓楼校区，排序正确")
        else:
            print(f"    ❌ 第一馆藏地不是鼓楼校区，排序可能有问题")
    
    return True

if __name__ == "__main__":
    print("开始测试搜索历史记录和校区排序功能...")
    
    # 测试搜索历史记录
    history_result = test_search_history()
    
    # 测试校区排序
    campus_result = test_campus_sorting()
    
    print("\n=== 测试总结 ===")
    print(f"搜索历史记录功能: {'✅ 正常' if history_result else '❌ 异常'}")
    print(f"校区排序功能: {'✅ 正常' if campus_result else '❌ 异常'}")
    
    if history_result and campus_result:
        print("\n🎉 所有测试通过！")
        exit(0)
    else:
        print("\n❌ 部分测试失败！")
        exit(1)