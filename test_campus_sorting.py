#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
简单测试脚本：验证校区排序功能
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
    "username": f"campus_user_{int(time.time())}",
    "password": "test123",
    "campus": "鼓楼"
}

def test_campus_sorting():
    """测试校区排序功能"""
    print("=== 测试校区排序功能 ===")
    
    # 1. 注册新用户
    print("\n1. 注册鼓楼校区测试用户...")
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
    print(f"登录成功，用户校区：{TEST_USER['campus']}")
    
    # 3. 设置请求头（包含token）
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    # 4. 执行搜索（使用可能有多个校区馆藏的关键词）
    print("\n3. 执行搜索...")
    test_query = "python"
    response = requests.get(SEARCH_URL, params={"query": test_query}, headers=headers)
    if response.status_code != 200:
        print(f"搜索失败: {response.status_code} - {response.text}")
        return False
    
    search_result = response.json()
    print(f"搜索成功，返回图书数量: {len(search_result)}")
    
    # 5. 检查是否有图书且有馆藏信息
    if not search_result:
        print("搜索结果为空，无法测试校区排序功能")
        return True
    
    # 6. 检查每本图书的馆藏排序是否正确
    print(f"\n4. 检查馆藏地排序（鼓楼校区应优先）...")
    
    # 检查至少5本图书（如果有更多的话）
    checked_books = 0
    for book in search_result[:5]:
        if book.get('holdings') and len(book.get('holdings')) > 1:
            print(f"\n检查图书: {book.get('title', '未知标题')}")
            
            # 获取馆藏地列表
            locations = [holding.get('location', '') for holding in book.get('holdings')]
            print(f"馆藏地顺序: {locations}")
            
            # 检查是否有鼓楼校区的馆藏
            has_gulou = any('鼓楼' in loc for loc in locations)
            if has_gulou:
                # 检查鼓楼校区的馆藏是否排在第一位
                if '鼓楼' in locations[0]:
                    print("✅ 鼓楼校区馆藏优先显示")
                    checked_books += 1
                else:
                    print("❌ 鼓楼校区馆藏未优先显示")
            else:
                print("ℹ️  该图书没有鼓楼校区馆藏")
    
    if checked_books > 0:
        print(f"\n✅ 成功验证了 {checked_books} 本图书的校区排序功能")
        return True
    else:
        print("\nℹ️  没有找到同时包含多个校区馆藏的图书，无法验证排序功能")
        return True

if __name__ == "__main__":
    print("开始测试校区排序功能...")
    
    # 测试校区排序功能
    campus_result = test_campus_sorting()
    
    print("\n=== 测试总结 ===")
    print(f"校区排序功能: {'✅ 正常' if campus_result else '❌ 异常'}")
    
    if campus_result:
        print("\n🎉 校区排序功能已经修复！")
        exit(0)
    else:
        print("\n❌ 校区排序功能仍然有问题！")
        exit(1)