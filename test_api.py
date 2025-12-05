#!/usr/bin/env python3
# 测试服务器API功能的脚本
import requests
import json
import time

test_server_url = "http://127.0.0.1:8080"

# 测试结果统计
tests_passed = 0
tests_failed = 0
total_tests = 0

# 测试注册功能
def test_register():
    global tests_passed, tests_failed, total_tests
    total_tests += 1
    
    print("\n=== 测试注册功能 ===")
    try:
        response = requests.post(
            f"{test_server_url}/api/register",
            json={
                "username": "testuser",
                "password": "testpassword",
                "campus": "仙林"
            },
            headers={"Content-Type": "application/json"}
        )
        
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        if response.status_code == 201:
            print("✓ 注册测试通过")
            tests_passed += 1
            return True
        else:
            print("✗ 注册测试失败")
            tests_failed += 1
            return False
            
    except Exception as e:
        print(f"✗ 注册测试失败: {e}")
        tests_failed += 1
        return False

# 测试登录功能
def test_login():
    global tests_passed, tests_failed, total_tests
    total_tests += 1
    
    print("\n=== 测试登录功能 ===")
    try:
        response = requests.post(
            f"{test_server_url}/api/login",
            json={
                "username": "testuser",
                "password": "testpassword"
            },
            headers={"Content-Type": "application/json"}
        )
        
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        if response.status_code == 200:
            print("✓ 登录测试通过")
            tests_passed += 1
            data = response.json()
            return data.get("access_token")
        else:
            print("✗ 登录测试失败")
            tests_failed += 1
            return None
            
    except Exception as e:
        print(f"✗ 登录测试失败: {e}")
        tests_failed += 1
        return None

# 测试获取校区功能
def test_get_campus():
    global tests_passed, tests_failed, total_tests
    total_tests += 1
    
    print("\n=== 测试获取校区功能 ===")
    try:
        response = requests.get(
            f"{test_server_url}/api/user/campus"
        )
        
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        if response.status_code == 200:
            print("✓ 获取校区测试通过")
            tests_passed += 1
            return True
        else:
            print("✗ 获取校区测试失败")
            tests_failed += 1
            return False
            
    except Exception as e:
        print(f"✗ 获取校区测试失败: {e}")
        tests_failed += 1
        return False

# 测试搜索功能
def test_search():
    global tests_passed, tests_failed, total_tests
    total_tests += 1
    
    print("\n=== 测试搜索功能 ===")
    try:
        response = requests.get(
            f"{test_server_url}/api/search",
            params={"query": "软件工程", "location": "图书馆"}
        )
        
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        if response.status_code == 200:
            print("✓ 搜索测试通过")
            tests_passed += 1
            return True
        else:
            print("✗ 搜索测试失败")
            tests_failed += 1
            return False
            
    except Exception as e:
        print(f"✗ 搜索测试失败: {e}")
        tests_failed += 1
        return False

# 测试获取历史记录功能
def test_history():
    global tests_passed, tests_failed, total_tests
    total_tests += 1
    
    print("\n=== 测试获取历史记录功能 ===")
    try:
        response = requests.get(
            f"{test_server_url}/api/search/history"
        )
        
        print(f"状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        if response.status_code == 200:
            print("✓ 历史记录测试通过")
            tests_passed += 1
            return True
        else:
            print("✗ 历史记录测试失败")
            tests_failed += 1
            return False
            
    except Exception as e:
        print(f"✗ 历史记录测试失败: {e}")
        tests_failed += 1
        return False

# 主函数
def main():
    print("开始测试服务器API功能...")
    print(f"测试服务器地址: {test_server_url}")
    
    # 等待服务器启动
    time.sleep(3)
    
    # 运行所有测试
    test_register()
    test_login()
    test_get_campus()
    test_search()
    test_history()
    
    # 打印测试结果
    print("\n" + "="*50)
    print("测试结果总结")
    print("="*50)
    print(f"总测试数: {total_tests}")
    print(f"通过测试: {tests_passed}")
    print(f"失败测试: {tests_failed}")
    
    if tests_failed == 0:
        print("\n🎉 所有测试通过！")
    else:
        print(f"\n⚠️  有 {tests_failed} 个测试失败")

if __name__ == "__main__":
    main()
