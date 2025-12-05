#!/usr/bin/env python3
# 最基本的HTTP服务器测试
import http.server
import socketserver
import os
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

PORT = 8081
# 切换到frontend目录
os.chdir('./frontend')
logger.info(f"切换到目录: {os.getcwd()}")

# 使用最基本的SimpleHTTPRequestHandler
handler = http.server.SimpleHTTPRequestHandler

# 创建服务器
with socketserver.TCPServer(("127.0.0.1", PORT), handler) as httpd:
    logger.info(f"服务器启动成功！")
    logger.info(f"访问地址: http://127.0.0.1:{PORT}")
    logger.info(f"按Ctrl+C停止服务器")
    
    # 启动服务器
    httpd.serve_forever()