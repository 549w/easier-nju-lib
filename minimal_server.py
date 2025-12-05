#!/usr/bin/env python3
# 最小化的前端服务器，只提供静态文件服务
import http.server
import socketserver
import os

PORT = 8000
FRONTEND_DIR = "frontend"

# 切换到前端目录
os.chdir(FRONTEND_DIR)

# 创建简单的HTTP服务器
handler = http.server.SimpleHTTPRequestHandler

# 使用TCPServer并设置允许地址重用
try:
    with socketserver.TCPServer(("127.0.0.1", PORT), handler) as httpd:
        print(f"前端服务器启动成功！")
        print(f"访问地址: http://127.0.0.1:{PORT}")
        print(f"按 Ctrl+C 停止服务器")
        httpd.serve_forever()
except KeyboardInterrupt:
    print("\n服务器已停止")
except Exception as e:
    print(f"服务器启动失败: {e}")
