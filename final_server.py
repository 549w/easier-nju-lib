#!/usr/bin/env python3
"""
南京大学图书馆一体化服务器 - 使用Flask框架
"""

import os
import sys
import logging
import json
import hashlib
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger('final_server')

# 设置路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, 'frontend')
PORT = 8081

# 导入南京大学图书馆OPAC爬虫模块
sys.path.append(os.path.join(BASE_DIR, 'backend'))
try:
    from opac_spider import OPACSpider
    logger.info("南京大学图书馆OPAC爬虫初始化完成")
except Exception as e:
    logger.error(f"南京大学图书馆OPAC爬虫初始化失败: {e}")
    sys.exit(1)

# 模拟数据库类
class MockDB:
    def __init__(self):
        self.users = []
        self.user_id_counter = 1
        self.search_history = []
    
    def add_user(self, username, password, campus=None):
        # 检查用户名是否已存在
        for user in self.users:
            if user[1] == username:
                raise Exception("用户名已存在")
        
        # 添加新用户
        user = [self.user_id_counter, username, password, campus]
        self.users.append(user)
        self.user_id_counter += 1
        return self.user_id_counter - 1
    
    def get_user(self, username):
        for user in self.users:
            if user[1] == username:
                return user
        return None
    
    def get_user_by_id(self, user_id):
        for user in self.users:
            if user[0] == user_id:
                return user
        return None
    
    def update_user_campus(self, user_id, campus):
        for user in self.users:
            if user[0] == user_id:
                user[3] = campus
                return True
        return False
    
    def add_search_history(self, user_id, query):
        self.search_history.append([user_id, query])
        return True
    
    def get_search_history(self, user_id):
        history = []
        for item in self.search_history:
            if item[0] == user_id:
                history.append(item[1])
        return history

# 初始化数据库
db = MockDB()

# 初始化爬虫
spider = OPACSpider()

# 创建Flask应用
app = Flask(__name__)
CORS(app)  # 启用CORS

# 密码加密函数
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# API路由
@app.route('/api/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        campus = data.get('campus')
        
        if not username or not password:
            return jsonify({'error': '用户名和密码不能为空'}), 400
            
        # 检查校区是否有效
        valid_campuses = ['鼓楼', '仙林', '浦口', '苏州']
        if campus and campus not in valid_campuses:
            return jsonify({'error': '无效的校区'}), 400
            
        # 加密密码
        hashed_password = hash_password(password)
        
        # 添加用户到数据库
        user_id = db.add_user(username, hashed_password, campus)
        
        return jsonify({
            'message': '注册成功',
            'access_token': username,
            'user': {
                'id': user_id,
                'username': username,
                'campus': campus
            }
        }), 201
        
    except Exception as e:
        logger.error(f"注册失败: {str(e)}")
        return jsonify({'error': str(e)}), 400

@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'error': '用户名和密码不能为空'}), 400
            
        # 加密密码
        hashed_password = hash_password(password)
        
        # 验证用户
        user = db.get_user(username)
        if not user or user[2] != hashed_password:
            return jsonify({'error': '用户名或密码错误'}), 401
            
        # 返回访问token和用户信息
        return jsonify({
            'message': '登录成功',
            'access_token': username,
            'user': {
                'id': user[0],
                'username': user[1],
                'campus': user[3]
            }
        }), 200
        
    except Exception as e:
        logger.error(f"登录失败: {str(e)}")
        return jsonify({'error': str(e)}), 400

@app.route('/api/user/campus', methods=['POST'])
def set_campus():
    try:
        data = request.get_json()
        
        # 首先尝试从请求体中获取用户名
        username = data.get('username')
        
        # 如果请求体中没有提供，尝试从Authorization头获取token（即用户名）
        if not username:
            auth_header = request.headers.get('Authorization')
            if auth_header and auth_header.startswith('Bearer '):
                username = auth_header.split(' ')[1]  # 获取Bearer后面的token
        
        campus = data.get('campus')
        
        if not username:
            return jsonify({'error': '未提供用户名'}), 400
            
        # 检查校区是否有效
        valid_campuses = ['鼓楼', '仙林', '浦口', '苏州']
        if campus and campus not in valid_campuses:
            return jsonify({'error': '无效的校区'}), 400
            
        # 获取用户信息
        user = db.get_user(username)
        if not user:
            return jsonify({'error': '用户不存在'}), 404
            
        # 更新用户校区
        db.update_user_campus(user[0], campus)
        
        return jsonify({'message': '校区设置成功', 'campus': campus}), 200
        
    except Exception as e:
        logger.error(f"校区设置失败: {str(e)}")
        return jsonify({'error': str(e)}), 400

@app.route('/api/user/campus', methods=['GET'])
def get_campus():
    try:
        # 首先尝试从URL参数获取用户名
        username = request.args.get('username')
        
        # 如果URL参数没有提供，尝试从Authorization头获取token（即用户名）
        if not username:
            auth_header = request.headers.get('Authorization')
            if auth_header and auth_header.startswith('Bearer '):
                username = auth_header.split(' ')[1]  # 获取Bearer后面的token
        
        if not username:
            return jsonify({'error': '未提供用户名'}), 400
            
        # 获取用户信息
        user = db.get_user(username)
        if not user:
            return jsonify({'error': '用户不存在'}), 404
            
        return jsonify({'campus': user[3]}), 200
        
    except Exception as e:
        logger.error(f"获取校区失败: {str(e)}")
        return jsonify({'error': str(e)}), 400

@app.route('/api/search', methods=['GET'])
def search_books():
    try:
        # 获取查询参数
        query = request.args.get('query', '')
        location = request.args.get('location', '')
        
        # 首先尝试从URL参数获取用户名
        username = request.args.get('username')
        
        # 如果URL参数没有提供，尝试从Authorization头获取token（即用户名）
        if not username:
            auth_header = request.headers.get('Authorization')
            if auth_header and auth_header.startswith('Bearer '):
                username = auth_header.split(' ')[1]  # 获取Bearer后面的token
        
        logger.info(f"收到搜索请求: query={query}, location={location}, username={username}")
        
        if not query:
            logger.warning("搜索关键词为空")
            return jsonify({'error': '请输入搜索关键词'}), 400
        
        # 使用爬虫搜索图书
        books = spider.search_books_by_title(query)
        
        # 如果用户已登录，获取用户校区设置并优先显示该校区的馆藏
        if username:
            user = db.get_user(username)
            if user:
                user_campus = user[3]
                # 如果用户设置了校区，优先显示该校区的馆藏
                if user_campus:
                    # 去除校区字符串中的空格
                    user_campus = user_campus.replace(' ', '')
                    valid_campuses = ['鼓楼', '仙林', '浦口', '苏州']
                    # 确保是有效的校区名称
                    if user_campus in valid_campuses:
                        for book in books:
                            if book.get('holdings'):
                                # 对馆藏信息进行排序，用户所在校区的馆藏优先显示
                                book['holdings'].sort(key=lambda x: 0 if user_campus in x['location'] else 1)
                                logger.info(f"为图书 '{book['title']}' 排序馆藏，优先显示 {user_campus} 校区的馆藏")
        
        # 根据馆藏地筛选图书
        if location:
            filtered_books = []
            for book in books:
                if book.get('holdings'):
                    # 筛选出包含指定馆藏地的图书
                    filtered_holdings = [holding for holding in book['holdings'] 
                                        if holding.get('location') and location in holding['location']]
                    if filtered_holdings:
                        # 如果有符合条件的馆藏，保留这本书并只显示符合条件的馆藏
                        filtered_book = book.copy()
                        filtered_book['holdings'] = filtered_holdings
                        filtered_books.append(filtered_book)
            books = filtered_books
            logger.info(f"馆藏地筛选完成，返回图书数量: {len(books)}")
        
        # 如果用户已登录，自动保存搜索历史
        if username:
            user = db.get_user(username)
            if user:
                db.add_search_history(user[0], query)
                logger.info(f"为用户 {username} 保存搜索历史: {query}")
        
        logger.info(f"搜索完成，返回图书数量: {len(books)}")
        return jsonify(books), 200
        
    except Exception as e:
        logger.error(f"搜索过程中出错: {str(e)}", exc_info=True)
        return jsonify({'error': f'服务器内部错误: {str(e)}'}), 500

@app.route('/api/search/history', methods=['GET'])
def get_search_history():
    try:
        # 首先尝试从URL参数获取用户名
        username = request.args.get('username')
        
        # 如果URL参数没有提供，尝试从Authorization头获取token（即用户名）
        if not username:
            auth_header = request.headers.get('Authorization')
            if auth_header and auth_header.startswith('Bearer '):
                username = auth_header.split(' ')[1]  # 获取Bearer后面的token
        
        if not username:
            return jsonify({'error': '未提供用户名'}), 400
            
        # 获取用户信息
        user = db.get_user(username)
        if not user:
            return jsonify({'error': '用户不存在'}), 404
            
        # 获取实际的搜索历史
        history = db.get_search_history(user[0])
        # 格式化历史记录，添加时间戳
        formatted_history = [{'query': item, 'search_time': '2023-12-05T10:00:00Z'} for item in history]
        return jsonify({'history': formatted_history}), 200
        
    except Exception as e:
        logger.error(f"获取搜索历史失败: {str(e)}")
        return jsonify({'error': str(e)}), 400

@app.route('/api/search/history', methods=['POST'])
def add_search_history():
    try:
        data = request.get_json()
        
        # 首先尝试从请求体中获取用户名
        username = data.get('username')
        query = data.get('query')
        
        # 如果请求体中没有提供，尝试从Authorization头获取token（即用户名）
        if not username:
            auth_header = request.headers.get('Authorization')
            if auth_header and auth_header.startswith('Bearer '):
                username = auth_header.split(' ')[1]  # 获取Bearer后面的token
        
        if not username:
            return jsonify({'error': '未提供用户名'}), 400
            
        if not query:
            return jsonify({'error': '未提供搜索关键词'}), 400
            
        # 获取用户信息
        user = db.get_user(username)
        if not user:
            return jsonify({'error': '用户不存在'}), 404
            
        # 保存搜索历史
        db.add_search_history(user[0], query)
        return jsonify({'message': '搜索历史已保存'}), 201
        
    except Exception as e:
        logger.error(f"保存搜索历史失败: {str(e)}")
        return jsonify({'error': str(e)}), 400

# 前端静态文件路由
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    """提供前端静态文件"""
    if path != "" and os.path.exists(os.path.join(FRONTEND_DIR, path)):
        return send_from_directory(FRONTEND_DIR, path)
    else:
        return send_from_directory(FRONTEND_DIR, 'index.html')

# 主程序
if __name__ == '__main__':
    try:
        # 确保前端目录存在
        if not os.path.exists(FRONTEND_DIR):
            logger.error(f"前端目录不存在: {FRONTEND_DIR}")
            sys.exit(1)
        
        logger.info(f"一体化服务器启动成功！")
        logger.info(f"访问地址: http://127.0.0.1:{PORT}")
        logger.info(f"前端目录: {FRONTEND_DIR}")
        logger.info(f"按 Ctrl+C 停止服务器")
        
        # 启动Flask服务器
        app.run(host='127.0.0.1', port=PORT, debug=False)
        
    except KeyboardInterrupt:
        logger.info("\n服务器已停止")
    except Exception as e:
        logger.error(f"服务器启动失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)