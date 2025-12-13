import sqlite3
import logging
import os
import datetime

# 配置日志
logger = logging.getLogger('OPACSpider')

db_path = 'library.db'

class Database:
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.connect()
        self.create_tables()
        
    def connect(self):
        """连接到SQLite数据库"""
        try:
            # 确保数据库目录存在
            db_dir = os.path.dirname(db_path)
            if db_dir and not os.path.exists(db_dir):
                os.makedirs(db_dir)
                
            self.conn = sqlite3.connect(db_path, check_same_thread=False)
            self.cursor = self.conn.cursor()
            logger.info(f"成功连接到数据库: {db_path}")
        except Exception as e:
            logger.error(f"连接数据库失败: {str(e)}")
            raise
    
    def create_tables(self):
        """创建用户表、搜索历史表和访问日志表"""
        try:
            # 创建用户表
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    campus TEXT DEFAULT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # 创建搜索历史表
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS search_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    query TEXT NOT NULL,
                    location TEXT DEFAULT '',
                    search_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id),
                    UNIQUE(user_id, query, location) ON CONFLICT REPLACE
                )
            ''')
            
            # 创建访问日志表
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS access_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    username TEXT DEFAULT NULL,
                    ip_address TEXT NOT NULL,
                    user_agent TEXT DEFAULT '',
                    request_path TEXT NOT NULL,
                    request_method TEXT DEFAULT 'GET',
                    status_code INTEGER DEFAULT 200,
                    access_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    ip_location TEXT DEFAULT '',
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            self.conn.commit()
            logger.info("数据库表创建完成")
        except Exception as e:
            logger.error(f"创建数据库表失败: {str(e)}")
            self.conn.rollback()
            raise
    
    def add_user(self, username, password, campus=None):
        """添加新用户"""
        try:
            self.cursor.execute(
                "INSERT INTO users (username, password, campus) VALUES (?, ?, ?)",
                (username, password, campus)
            )
            self.conn.commit()
            logger.info(f"用户注册成功: {username}")
            return self.cursor.lastrowid
        except sqlite3.IntegrityError as e:
            logger.error(f"用户注册失败 - 用户名已存在: {username}")
            self.conn.rollback()
            raise Exception("用户名已存在")
        except Exception as e:
            logger.error(f"用户注册失败: {str(e)}")
            self.conn.rollback()
            raise
    
    def get_user(self, username):
        """根据用户名获取用户信息"""
        try:
            self.cursor.execute(
                "SELECT id, username, password, campus FROM users WHERE username = ?",
                (username,)
            )
            return self.cursor.fetchone()
        except Exception as e:
            logger.error(f"获取用户信息失败: {str(e)}")
            raise
    
    def get_user_by_id(self, user_id):
        """根据用户ID获取用户信息"""
        try:
            self.cursor.execute(
                "SELECT id, username, password, campus FROM users WHERE id = ?",
                (user_id,)
            )
            return self.cursor.fetchone()
        except Exception as e:
            logger.error(f"根据ID获取用户信息失败: {str(e)}")
            raise
    
    def update_user_campus(self, user_id, campus):
        """更新用户校区设置"""
        try:
            self.cursor.execute(
                "UPDATE users SET campus = ? WHERE id = ?",
                (campus, user_id)
            )
            self.conn.commit()
            logger.info(f"用户校区更新成功: user_id={user_id}, campus={campus}")
            return True
        except Exception as e:
            logger.error(f"更新用户校区失败: {str(e)}")
            self.conn.rollback()
            raise
    
    def add_search_history(self, user_id, query, location=''):
        """添加搜索历史记录，自动去重"""
        try:
            self.cursor.execute(
                "INSERT INTO search_history (user_id, query, location) VALUES (?, ?, ?)",
                (user_id, query, location)
            )
            self.conn.commit()
            logger.info(f"搜索历史记录添加成功: user_id={user_id}, query={query}, location={location}")
            return True
        except Exception as e:
            logger.error(f"添加搜索历史记录失败: {str(e)}")
            self.conn.rollback()
            raise
    
    def get_search_history(self, user_id, limit=20):
        """获取用户的搜索历史记录"""
        try:
            self.cursor.execute(
                "SELECT id, query, location, search_time FROM search_history WHERE user_id = ? ORDER BY search_time DESC LIMIT ?",
                (user_id, limit)
            )
            # 将元组列表转换为字典列表
            results = []
            for row in self.cursor.fetchall():
                results.append({
                    'id': row[0],
                    'query': row[1],
                    'location': row[2],
                    'search_time': row[3]
                })
            return results
        except Exception as e:
            logger.error(f"获取搜索历史记录失败: {str(e)}")
            raise
    
    def delete_search_history(self, user_id, history_id):
        """删除单条搜索历史记录"""
        try:
            self.cursor.execute(
                "DELETE FROM search_history WHERE user_id = ? AND id = ?",
                (user_id, history_id)
            )
            self.conn.commit()
            logger.info(f"搜索历史记录删除成功: user_id={user_id}, history_id={history_id}")
            return True
        except Exception as e:
            logger.error(f"删除搜索历史记录失败: {str(e)}")
            self.conn.rollback()
            raise
    
    def clear_search_history(self, user_id):
        """清空用户的所有搜索历史记录"""
        try:
            self.cursor.execute(
                "DELETE FROM search_history WHERE user_id = ?",
                (user_id,)
            )
            self.conn.commit()
            logger.info(f"搜索历史记录清空成功: user_id={user_id}")
            return True
        except Exception as e:
            logger.error(f"清空搜索历史记录失败: {str(e)}")
            self.conn.rollback()
            raise
    
    def add_access_log(self, user_id=None, username=None, ip_address='', user_agent='', 
                      request_path='', request_method='GET', status_code=200, ip_location=''):
        """添加访问日志记录"""
        try:
            # 简化IP属地功能，暂时不获取具体位置
            ip_location = ''  # 默认空字符串
            self.cursor.execute(
                "INSERT INTO access_logs (user_id, username, ip_address, user_agent, "
                "request_path, request_method, status_code, ip_location) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (user_id, username, ip_address, user_agent, request_path, 
                 request_method, status_code, ip_location)
            )
            self.conn.commit()
            logger.info(f"访问日志记录添加成功: user_id={user_id}, username={username}, ip={ip_address}")
            return True
        except Exception as e:
            logger.error(f"添加访问日志记录失败: {str(e)}")
            self.conn.rollback()
            raise
    
    def get_all_users(self):
        """获取所有用户信息（不包含密码）"""
        try:
            self.cursor.execute(
                "SELECT id, username, campus, created_at FROM users ORDER BY created_at DESC"
            )
            results = []
            for row in self.cursor.fetchall():
                results.append({
                    'id': row[0],
                    'username': row[1],
                    'campus': row[2],
                    'created_at': row[3]
                })
            return results
        except Exception as e:
            logger.error(f"获取所有用户信息失败: {str(e)}")
            raise
    
    def get_all_access_logs(self, limit=1000):
        """获取所有访问日志记录"""
        try:
            self.cursor.execute(
                "SELECT id, user_id, username, ip_address, user_agent, request_path, "
                "request_method, status_code, access_time, ip_location "
                "FROM access_logs ORDER BY access_time DESC LIMIT ?",
                (limit,)
            )
            results = []
            for row in self.cursor.fetchall():
                results.append({
                    'id': row[0],
                    'user_id': row[1],
                    'username': row[2],
                    'ip_address': row[3],
                    'user_agent': row[4],
                    'request_path': row[5],
                    'request_method': row[6],
                    'status_code': row[7],
                    'access_time': row[8],
                    'ip_location': row[9]
                })
            return results
        except Exception as e:
            logger.error(f"获取所有访问日志记录失败: {str(e)}")
            raise
    
    def get_statistics(self):
        """获取统计信息：账号总量、访问总量、搜索总量"""
        try:
            # 获取账号总量
            self.cursor.execute("SELECT COUNT(*) FROM users")
            user_count = self.cursor.fetchone()[0]
            
            # 获取访问总量
            self.cursor.execute("SELECT COUNT(*) FROM access_logs")
            access_count = self.cursor.fetchone()[0]
            
            # 获取搜索总量
            self.cursor.execute("SELECT COUNT(*) FROM search_history")
            search_count = self.cursor.fetchone()[0]
            
            return {
                'user_count': user_count,
                'access_count': access_count,
                'search_count': search_count
            }
        except Exception as e:
            logger.error(f"获取统计信息失败: {str(e)}")
            raise
    
    def get_user_access_logs(self, user_id, limit=100):
        """获取指定用户的访问日志记录"""
        try:
            self.cursor.execute(
                "SELECT id, ip_address, user_agent, request_path, request_method, "
                "status_code, access_time, ip_location "
                "FROM access_logs WHERE user_id = ? ORDER BY access_time DESC LIMIT ?",
                (user_id, limit)
            )
            results = []
            for row in self.cursor.fetchall():
                results.append({
                    'id': row[0],
                    'ip_address': row[1],
                    'user_agent': row[2],
                    'request_path': row[3],
                    'request_method': row[4],
                    'status_code': row[5],
                    'access_time': row[6],
                    'ip_location': row[7]
                })
            return results
        except Exception as e:
            logger.error(f"获取用户访问日志记录失败: {str(e)}")
            raise
    
    def close(self):
        """关闭数据库连接"""
        if self.conn:
            self.conn.close()
            logger.info("数据库连接已关闭")

# 创建全局数据库实例
db = Database()