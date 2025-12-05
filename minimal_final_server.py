#!/usr/bin/env python3
# 极简版final_server测试
import sys
import os
import logging
from http.server import HTTPServer, SimpleHTTPRequestHandler

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('minimal_server')

PORT = 8081
FRONTEND_DIR = os.path.join(os.path.dirname(__file__), 'frontend')

# 自定义请求处理器
class MinimalHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        kwargs['directory'] = FRONTEND_DIR
        super().__init__(*args, **kwargs)
    
    def do_GET(self):
        logger.info(f"处理GET请求: {self.path}")
        if self.path.startswith('/api/'):
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(b'{"message": "Hello, API!"}')
        else:
            if '.' not in self.path.split('/')[-1]:
                self.path = '/index.html'
            super().do_GET()

# 主程序
if __name__ == '__main__':
    try:
        logger.info(f"启动极简服务器，端口: {PORT}")
        server_address = ('127.0.0.1', PORT)
        httpd = HTTPServer(server_address, MinimalHandler)
        
        logger.info("服务器启动成功！")
        logger.info(f"访问地址: http://127.0.0.1:{PORT}")
        
        # 启动服务器
        httpd.serve_forever()
        
    except KeyboardInterrupt:
        logger.info("\n服务器已停止")
    except Exception as e:
        logger.error(f"服务器错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)