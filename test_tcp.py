#!/usr/bin/env python3
# 最基本的TCP测试脚本
import socket
import sys

print(f"Python版本: {sys.version}")

# 创建一个简单的TCP socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("✓ 创建socket成功")
    
    # 绑定到端口
    s.bind(('127.0.0.1', 8000))
    print("✓ 绑定到127.0.0.1:8000成功")
    
    # 开始监听
    s.listen(1)
    print("✓ 开始监听...")
    print("✓ 按Ctrl+C停止")
    
    # 接受一个连接
    conn, addr = s.accept()
    print(f"✓ 接受连接: {addr}")
    
    # 发送响应
    conn.sendall(b"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<!DOCTYPE html><html><body><h1>Hello, World!</h1></body></html>")
    print("✓ 发送响应成功")
    
    # 关闭连接
    conn.close()
    print("✓ 关闭连接")
    
    # 继续监听
    s.listen(1)
    print("✓ 继续监听...")
    
except Exception as e:
    print(f"✗ 错误: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
finally:
    s.close()
    print("✓ 关闭socket")