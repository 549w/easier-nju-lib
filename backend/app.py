from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import sys
import logging
import os
import json
import hashlib

# 配置日志 - 同时输出到控制台和文件
import logging.handlers
log_dir = 'logs'
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, 'app.log')

# 创建logger实例
logger = logging.getLogger()  # 获取根logger
logger.setLevel(logging.DEBUG)

# 创建控制台处理器
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# 创建RotatingFileHandler，避免文件占用问题
file_handler = logging.handlers.RotatingFileHandler(
    'logs/app.log',
    maxBytes=10*1024*1024,  # 10MB
    backupCount=5,
    encoding='utf-8'
)
file_handler.setLevel(logging.DEBUG)  # 文件记录所有DEBUG及以上级别

# 设置日志格式
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# 清除可能已存在的处理器
if logger.handlers:
    logger.handlers.clear()

# 添加处理器到根logger
logger.addHandler(console_handler)
logger.addHandler(file_handler)

# 确保OPACSpider的日志也能被记录
oac_spider_logger = logging.getLogger('OPACSpider')
oac_spider_logger.setLevel(logging.DEBUG)

logger.info('应用启动，日志系统初始化完成')

# 先创建Flask应用实例
app = Flask(__name__)

# 启用CORS，允许跨域请求
CORS(app)

# JWT配置
app.config['JWT_SECRET_KEY'] = 'nju-lib-secret-key'  # 生产环境中应使用更安全的密钥
jwt = JWTManager(app)

# 导入数据库
from database import db

# 添加异常处理（暂时注释掉，测试是否是异常处理导致问题）
# @app.errorhandler(Exception)
# def handle_exception(e):
#     logger.error(f'未捕获的异常: {str(e)}')
#     return jsonify({'error': '服务器内部错误'}), 500

# 导入南京大学图书馆OPAC爬虫模块
from opac_spider import spider

logger.info('南京大学图书馆OPAC爬虫初始化完成')

# 密码加密函数
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# 暂时移除测试路由，避免可能的路由冲突

@app.route('/api/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        campus = data.get('campus')
        
        print(f"\n=== 注册请求调试信息 ===")
        print(f"原始请求数据: {data}")
        print(f"username: {username}")
        print(f"password: {'***' if password else 'None'}")
        print(f"campus: '{campus}'")
        
        if not username or not password:
            return jsonify({'error': '用户名和密码不能为空'}), 400
            
        # 完全移除校区验证，直接处理注册
        print("校区验证已完全移除，继续处理注册...")
        
        # 不修改campus值，直接使用接收到的内容
            
        # 加密密码
        hashed_password = hash_password(password)
        
        # 添加用户到数据库
        user_id = db.add_user(username, hashed_password, campus)
        
        # 获取刚创建的用户信息
        user = db.get_user(username)
        
        # 创建访问令牌
        access_token = create_access_token(identity=str(user[0]))
        
        return jsonify({
            'message': '注册成功',
            'access_token': access_token,
            'user': {
                'id': user[0],
                'username': user[1],
                'campus': user[3]
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
            
        # 创建访问令牌
        access_token = create_access_token(identity=str(user[0]))
        
        # 返回用户信息和令牌
        return jsonify({
            'message': '登录成功',
            'access_token': access_token,
            'user': {
                'id': user[0],
                'username': user[1],
                'campus': user[3]
            }
        })
        
    except Exception as e:
        logger.error(f"登录失败: {str(e)}")
        return jsonify({'error': str(e)}), 400

@app.route('/api/user/campus', methods=['POST'])
@jwt_required()
def set_campus():
    try:
        user_id = get_jwt_identity()
        
        data = request.get_json()
        campus = data.get('campus')
        
        # 检查校区是否有效
        valid_campuses = ['鼓楼', '仙林', '浦口', '苏州']
        if not campus or campus not in valid_campuses:
            return jsonify({'error': '无效的校区'}), 400
            
        # 更新用户校区
        db.update_user_campus(user_id, campus)
        
        return jsonify({'message': '校区设置成功', 'campus': campus})
        
    except Exception as e:
        logger.error(f"校区设置失败: {str(e)}")
        return jsonify({'error': str(e)}), 400

# 移除重复的路由定义

@app.route('/api/search', methods=['GET'])
@jwt_required(optional=True)  # 使用optional=True允许未登录用户访问
def search_books():
    try:
        # 获取当前用户信息（如果已登录）
        user_id = get_jwt_identity()
        username = None
        if user_id:
            # 如果已登录，从数据库获取用户名
            user = db.get_user_by_id(int(user_id))
            if user:
                username = user[1]
            logger.info(f"已登录用户: user_id={user_id}, username={username}")
        else:
            logger.info("未登录用户访问")
        
        # 获取查询参数
        query = request.args.get('query', '')
        location = request.args.get('location', '')  # 获取馆藏地筛选参数
        logger.info(f"收到搜索请求: query={query}, location={location}, user_id={user_id}")
        
        if not query:
            logger.warning("搜索关键词为空")
            return jsonify({'error': '请输入搜索关键词'}), 400
        
        # 使用爬虫搜索图书
        books = spider.search_books_by_title(query)
        
        # 如果用户已登录，获取用户校区设置并优先显示该校区的馆藏
        if user_id:
            user = db.get_user_by_id(int(user_id))
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
        
        # 如果用户已登录，记录搜索历史
        if user_id:
            db.add_search_history(int(user_id), query, location)
        
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
        
        logger.info(f"搜索完成，返回图书数量: {len(books)}")
        return jsonify(books)
        
    except Exception as e:
        logger.error(f"搜索过程中出错: {str(e)}", exc_info=True)
        return jsonify({'error': f'服务器内部错误: {str(e)}'}), 500

@app.route('/', methods=['GET'])
def index():
    return jsonify({'message': '南京大学图书馆检索API服务'})

@app.route('/api/set-campus', methods=['PUT'])
@jwt_required()
def set_campus_new():
    try:
        user_id = int(get_jwt_identity())
        data = request.get_json()
        campus = data.get('campus')
        
        # 验证校区是否有效（去除空格）
        valid_campuses = ['鼓楼', '仙林', '浦口', '苏州']
        if campus:
            # 去除校区字符串中的空格
            campus = campus.replace(' ', '')
            if campus not in valid_campuses:
                logger.warning(f"无效的校区: {campus}")
                return jsonify({'error': '无效的校区'}), 400
        
        # 更新用户校区设置
        db.update_user_campus(user_id, campus)
        logger.info(f"更新用户校区设置: user_id={user_id}, campus={campus}")
        return jsonify({'message': '校区设置已更新', 'campus': campus})
    except Exception as e:
        logger.error(f"更新校区设置失败: {e}")
        return jsonify({'error': '更新校区设置失败'}), 500

# 已移除重复的路由定义

@app.route('/api/search-history', methods=['GET'])
@jwt_required()
def get_search_history():
    try:
        user_id = get_jwt_identity()
        
        # 获取搜索历史
        history = db.get_search_history(int(user_id))
        
        return jsonify({'history': history})
        
    except Exception as e:
        logger.error(f"获取搜索历史失败: {str(e)}")
        return jsonify({'error': str(e)}), 400

# @app.route('/api/search/history', methods=['GET'])  # 重复路径，已注释
# @jwt_required()
# def get_search_history_alt():
#     """兼容前端的搜索历史API路径"""
#     return get_search_history()

@app.route('/api/search-history/<int:history_id>', methods=['DELETE'])
@jwt_required()
def delete_search_history(history_id):
    try:
        user_id = get_jwt_identity()
        
        # 删除单条搜索历史记录
        db.delete_search_history(int(user_id), history_id)
        
        return jsonify({'message': '搜索历史记录已删除'})
        
    except Exception as e:
        logger.error(f"删除搜索历史记录失败: {str(e)}")
        return jsonify({'error': str(e)}), 400

@app.route('/api/search-history', methods=['DELETE'])
@jwt_required()
def clear_search_history():
    try:
        user_id = get_jwt_identity()
        
        # 清空所有搜索历史记录
        db.clear_search_history(int(user_id))
        
        return jsonify({'message': '所有搜索历史记录已清空'})
        
    except Exception as e:
        logger.error(f"清空搜索历史记录失败: {str(e)}")
        return jsonify({'error': str(e)}), 400

@app.route('/api/user/campus', methods=['GET'])
@jwt_required()
def get_user_campus():
    """获取用户校区设置"""
    try:
        user_id = get_jwt_identity()
        user = db.get_user_by_id(int(user_id))
        if user:
            return jsonify({'campus': user[3]})
        return jsonify({'campus': None}), 404
    except Exception as e:
        logger.error(f"获取用户校区失败: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/test', methods=['GET'])
def test_api():
    return jsonify({'message': 'API测试成功', 'status': 'ok'})

@app.route('/test', methods=['GET'])
def test():
    return jsonify({'message': '测试路由成功', 'status': 'ok'})

if __name__ == '__main__':
    # 开启debug模式以获取详细错误信息
    app.run(host='0.0.0.0', port=5005, debug=False)