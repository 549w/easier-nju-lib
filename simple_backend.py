#!/usr/bin/env python3
# 简化的后端API服务器
import sys
import os
import json
import hashlib

# 将backend目录添加到路径
backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.append(backend_dir)

# 设置日志
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('simple_backend')

# 创建数据库实例
logger.info("正在初始化数据库...")
try:
    from database import Database
    db = Database()
    logger.info("数据库初始化成功")
except Exception as e:
    logger.error(f"数据库初始化失败: {e}")
    sys.exit(1)

# 创建爬虫实例
logger.info("正在初始化OPAC爬虫...")
try:
    from opac_spider import OPACSpider
    spider = OPACSpider()
    logger.info("OPAC爬虫初始化成功")
except Exception as e:
    logger.error(f"OPAC爬虫初始化失败: {e}")
    sys.exit(1)

# 密码加密函数
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# 创建简单的HTTP服务器
from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse

class SimpleAPIHandler(BaseHTTPRequestHandler):
    def send_response_json(self, status_code, data):
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
    
    def do_POST(self):
        if self.path == '/api/register':
            self.handle_register()
        elif self.path == '/api/login':
            self.handle_login()
        else:
            self.send_response(404)
            self.end_headers()
    
    def do_GET(self):
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path
        params = urllib.parse.parse_qs(parsed_path.query)
        
        if path == '/api/search':
            self.handle_search(params)
        elif path == '/api/search/history':
            self.handle_search_history(params)
        elif path == '/api/user/campus':
            self.handle_get_campus(params)
        else:
            self.send_response(404)
            self.end_headers()
    
    def handle_register(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            
            username = data.get('username')
            password = data.get('password')
            campus = data.get('campus')
            
            if not username or not password:
                self.send_response_json(400, {'error': '用户名和密码不能为空'})
                return
            
            # 加密密码
            hashed_password = hash_password(password)
            
            # 添加用户
            user_id = db.add_user(username, hashed_password, campus)
            self.send_response_json(201, {'message': '注册成功', 'user_id': user_id})
        except json.JSONDecodeError:
            self.send_response_json(400, {'error': '无效的JSON数据'})
        except Exception as e:
            logger.error(f'注册失败: {e}')
            self.send_response_json(500, {'error': str(e)})
    
    def handle_login(self):
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data)
            
            username = data.get('username')
            password = data.get('password')
            
            if not username or not password:
                self.send_response_json(400, {'error': '用户名和密码不能为空'})
                return
            
            # 验证用户
            user = db.get_user(username)
            if not user or user[2] != hash_password(password):
                self.send_response_json(401, {'error': '用户名或密码错误'})
                return
            
            # 简单的认证（不使用JWT）
            self.send_response_json(200, {'access_token': username})
        except json.JSONDecodeError:
            self.send_response_json(400, {'error': '无效的JSON数据'})
        except Exception as e:
            logger.error(f'登录失败: {e}')
            self.send_response_json(500, {'error': str(e)})
    
    def handle_search(self, params):
        try:
            # 获取查询参数
            query = params.get('query', [''])[0]
            location = params.get('location', [''])[0]
            
            if not query:
                self.send_response_json(400, {'error': '搜索关键词不能为空'})
                return
            
            # 简化的搜索功能
            books = spider.search_books(query, location=location, campus='仙林')
            self.send_response_json(200, books)
        except Exception as e:
            logger.error(f'搜索失败: {e}')
            self.send_response_json(500, {'error': str(e)})
    
    def handle_search_history(self, params):
        try:
            # 简化的历史记录功能
            self.send_response_json(200, {'history': []})
        except Exception as e:
            logger.error(f'获取历史记录失败: {e}')
            self.send_response_json(500, {'error': str(e)})
    
    def handle_get_campus(self, params):
        try:
            # 简化的校区获取功能
            self.send_response_json(200, {'campus': '仙林'})
        except Exception as e:
            logger.error(f'获取校区失败: {e}')
            self.send_response_json(500, {'error': str(e)})

# 确保数据库创建db实例
if __name__ == '__main__':
    PORT = 5000
    
    try:
        server = HTTPServer(('127.0.0.1', PORT), SimpleAPIHandler)
        logger.info(f'简化的后端服务器启动成功！')
        logger.info(f'API地址: http://127.0.0.1:{PORT}/api/')
        logger.info(f'按 Ctrl+C 停止服务器')
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info("\n服务器已停止")
    except Exception as e:
        logger.error(f"服务器启动失败: {e}")
