#!/usr/bin/env python3
# 一体化服务器，同时提供前端静态文件和后端API功能
from flask import Flask, request, jsonify, send_from_directory
import sys
import logging
import os
import hashlib

# 设置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 创建Flask应用实例
app = Flask(__name__, static_folder='frontend', static_url_path='')

# 启用CORS（虽然在同一服务器下不需要，但为了兼容性保留）
from flask_cors import CORS
CORS(app)

# JWT配置
app.config['JWT_SECRET_KEY'] = 'nju-lib-secret-key'  # 生产环境中应使用更安全的密钥
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
jwt = JWTManager(app)

# 导入数据库
import sys
sys.path.append('backend')
from database import db

# 导入南京大学图书馆OPAC爬虫模块
from opac_spider import spider

logger.info('南京大学图书馆OPAC爬虫初始化完成')

# 密码加密函数
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# 后端API路由
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
        return jsonify({'message': '注册成功', 'user_id': user_id}), 201
    except Exception as e:
        logger.error(f'注册失败: {str(e)}')
        return jsonify({'error': '注册失败'}), 500

@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'error': '用户名和密码不能为空'}), 400
            
        # 验证用户
        user = db.get_user(username)
        if not user or user[2] != hash_password(password):
            return jsonify({'error': '用户名或密码错误'}), 401
            
        # 创建JWT token
        access_token = create_access_token(identity=username)
        return jsonify({'access_token': access_token}), 200
    except Exception as e:
        logger.error(f'登录失败: {str(e)}')
        return jsonify({'error': '登录失败'}), 500

@app.route('/api/user/campus', methods=['GET'])
@jwt_required()
def get_user_campus():
    try:
        current_user = get_jwt_identity()
        user = db.get_user(current_user)
        if not user:
            return jsonify({'error': '用户不存在'}), 404
            
        return jsonify({'campus': user[3]}), 200
    except Exception as e:
        logger.error(f'获取用户校区失败: {str(e)}')
        return jsonify({'error': '获取用户校区失败'}), 500

@app.route('/api/search', methods=['GET'])
@jwt_required()
def search_books():
    try:
        current_user = get_jwt_identity()
        query = request.args.get('query')
        location = request.args.get('location')
        
        if not query:
            return jsonify({'error': '搜索关键词不能为空'}), 400
            
        # 获取用户校区
        user = db.get_user(current_user)
        if not user:
            return jsonify({'error': '用户不存在'}), 404
            
        user_campus = user[3] if user[3] else '仙林'  # 默认仙林校区
        
        # 搜索图书
        books = spider.search_books(query, location=location, campus=user_campus)
        
        # 记录搜索历史
        db.add_search_history(current_user, query, location)
        
        return jsonify(books), 200
    except Exception as e:
        logger.error(f'搜索失败: {str(e)}')
        return jsonify({'error': '搜索失败'}), 500

@app.route('/api/search/history', methods=['GET'])
@jwt_required()
def get_search_history():
    try:
        current_user = get_jwt_identity()
        history = db.get_search_history(current_user)
        
        # 格式化时间
        formatted_history = []
        for item in history:
            formatted_history.append({
                'id': item[0],
                'query': item[2],
                'location': item[3],
                'search_time': item[4].strftime('%Y-%m-%d %H:%M:%S') if item[4] else None
            })
            
        return jsonify({'history': formatted_history}), 200
    except Exception as e:
        logger.error(f'获取搜索历史失败: {str(e)}')
        return jsonify({'error': '获取搜索历史失败'}), 500

# 前端路由 - 所有其他路径都返回前端首页
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    if path != '' and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    logger.info('一体化服务器启动成功！')
    logger.info('前端访问地址: http://127.0.0.1:8000')
    logger.info('后端API地址: http://127.0.0.1:8000/api/')
    app.run(host='127.0.0.1', port=8000, debug=False)
