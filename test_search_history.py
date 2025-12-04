#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单测试脚本：验证搜索历史记录功能
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
        # 即使搜索失败，也要尝试获取搜索历史，因为搜索历史可能已经记录了
    else:
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

if __name__ == "__main__":
    print("开始测试搜索历史记录功能...")
    
    # 测试搜索历史记录
    history_result = test_search_history()
    
    print("\n=== 测试总结 ===")
    print(f"搜索历史记录功能: {'✅ 正常' if history_result else '❌ 异常'}")
    
    if history_result:
        print("\n🎉 搜索历史记录功能已经修复！")
        exit(0)
    else:
        print("\n❌ 搜索历史记录功能仍然有问题！")
        exit(1)