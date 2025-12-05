#!/usr/bin/env python3
import requests
import json

# 测试API地址
BASE_URL = 'http://localhost:8081/api'

def test_register():
    """测试注册功能"""
    print("=== 测试注册功能 ===")
    url = f'{BASE_URL}/register'
    data = {
        'username': 'test_user',
        'password': 'test_password',
        'campus': '鼓楼'
    }
    response = requests.post(url, json=data)
    print(f"状态码: {response.status_code}")
    
    if response.status_code == 201:
        data = response.json()
        print("注册成功！")
        print(f"用户信息: {json.dumps(data['user'], ensure_ascii=False)}")
        return True
    else:
        print(f"注册失败: {response.json().get('error', '未知错误')}")
        return False

def test_login():
    """测试登录功能"""
    print("\n=== 测试登录功能 ===")
    url = f'{BASE_URL}/login'
    data = {
        'username': 'test_user',
        'password': 'test_password'
    }
    response = requests.post(url, json=data)
    print(f"状态码: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print("登录成功！")
        print(f"用户信息: {json.dumps(data['user'], ensure_ascii=False)}")
        print(f"访问令牌: {data['access_token']}")
        return data['access_token']
    else:
        print(f"登录失败: {response.json().get('error', '未知错误')}")
        return None

def test_get_user_info(token):
    """测试获取用户信息功能"""
    print("\n=== 测试获取用户信息功能 ===")
    url = f'{BASE_URL}/user/campus'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(url, headers=headers)
    print(f"状态码: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"用户信息: {json.dumps(data, ensure_ascii=False)}")
        return True
    else:
        print(f"获取用户信息失败: {response.json().get('error', '未知错误')}")
        return False

if __name__ == "__main__":
    # 先尝试注册
    register_success = test_register()
    
    # 然后尝试登录
    token = test_login()
    
    # 如果登录成功，测试获取用户信息
    if token:
        test_get_user_info(token)
    
    print("\n=== 测试完成 ===")
