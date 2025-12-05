#!/usr/bin/env python3
# 简单的一体化服务器，同时提供前端文件和后端API
import http.server
import socketserver
import urllib.parse
import requests
import os

PORT = 8000
BACKEND_URL = "http://127.0.0.1:5001"
FRONTEND_DIR = "frontend"

class SimpleHTTPProxy(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # 处理API请求
        if self.path.startswith('/api/'):
            self.handle_api_request()
        else:
            # 处理前端文件请求
            super().do_GET()
    
    def do_POST(self):
        # 处理API请求
        if self.path.startswith('/api/'):
            self.handle_api_request()
        else:
            super().do_POST()
    
    def handle_api_request(self):
        # 构建目标URL
        target_url = BACKEND_URL + self.path
        
        try:
            # 获取请求体
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length) if content_length > 0 else None
            
            # 构建请求头
            headers = {k: v for k, v in self.headers.items() if k.lower() not in ['host', 'content-length']}
            
            # 发送请求到后端
            response = requests.request(
                self.command,
                target_url,
                headers=headers,
                data=body,
                allow_redirects=False
            )
            
            # 发送响应给客户端
            self.send_response(response.status_code)
            for k, v in response.headers.items():
                if k.lower() not in ['transfer-encoding']:
                    self.send_header(k, v)
            self.end_headers()
            self.wfile.write(response.content)
            
        except Exception as e:
            self.send_error(500, f'Proxy error: {str(e)}')

# 切换到前端目录
os.chdir(FRONTEND_DIR)

# 启动服务器
with socketserver.TCPServer(("", PORT), SimpleHTTPProxy) as httpd:
    print(f"一体化服务器启动成功！")
    print(f"前端访问地址: http://localhost:{PORT}")
    print(f"后端API代理: http://localhost:{PORT}/api/")
    print(f"按 Ctrl+C 停止服务器")
    httpd.serve_forever()
