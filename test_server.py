#!/usr/bin/env python3
# 最简单的测试服务器，只测试基本HTTP功能
import http.server
import socketserver
import os
import sys

PORT = 8000

# 确保在当前目录
print(f"当前工作目录: {os.getcwd()}")
print(f"Python版本: {sys.version}")
print(f"准备在端口 {PORT} 启动测试服务器...")

try:
    # 创建简单的HTTP服务器
    handler = http.server.SimpleHTTPRequestHandler
    
    # 使用TCPServer
    with socketserver.TCPServer(("127.0.0.1", PORT), handler) as httpd:
        print(f"✓ 测试服务器启动成功！")
        print(f"✓ 访问地址: http://127.0.0.1:{PORT}")
        print(f"✓ 按 Ctrl+C 停止服务器")
        
        # 尝试服务一个请求
        print(f"\n等待第一个请求...")
        httpd.handle_request()  # 只处理一个请求
        print(f"✓ 成功处理了一个请求")
        
        # 继续运行
        print(f"继续运行服务器...")
        httpd.serve_forever()
        
except Exception as e:
    print(f"✗ 服务器启动失败: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
except KeyboardInterrupt:
    print("\n✓ 服务器已停止")
