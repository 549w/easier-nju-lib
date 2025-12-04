import requests
import logging
import time
from urllib.parse import urljoin, quote
import re
import json

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('SPA_Analyzer')

class SPAAnalyzer:
    def __init__(self):
        self.session = requests.Session()
        self.session.verify = False
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Referer': 'https://opac.nju.edu.cn/',
            'Connection': 'keep-alive'
        }
        self.base_url = 'https://opac.nju.edu.cn'
    
    def analyze_spa_search(self, search_term):
        """分析SPA应用的搜索机制"""
        logger.info(f"开始分析SPA应用，搜索词: {search_term}")
        
        # 首先，获取初始页面
        initial_url = self.base_url
        logger.info(f"获取初始页面: {initial_url}")
        
        try:
            response = self.session.get(initial_url, timeout=15)
            if response.status_code != 200:
                logger.error(f"获取初始页面失败，状态码: {response.status_code}")
                return
            
            # 分析页面中的JavaScript文件
            js_files = re.findall(r'<script[^>]+src="?([^>"\s]+)"?[^>]*>', response.text)
            logger.info(f"找到 {len(js_files)} 个JavaScript文件")
            
            # 保存初始页面
            with open('initial_page.html', 'w', encoding='utf-8') as f:
                f.write(response.text)
            logger.info("初始页面已保存到 initial_page.html")
            
            # 查找可能包含API调用信息的JavaScript文件
            for i, js_file in enumerate(js_files[:5]):  # 只分析前5个文件，避免过多请求
                js_url = js_file if js_file.startswith('http') else urljoin(self.base_url, js_file)
                logger.info(f"分析JavaScript文件 {i+1}/{len(js_files)}: {js_url}")
                
                try:
                    js_response = self.session.get(js_url, timeout=15)
                    if js_response.status_code == 200:
                        # 搜索API相关的代码
                        api_patterns = [
                            r'/api/',
                            r'fetch\(',
                            r'axios\.(get|post|request)',
                            r'\.ajax\(',
                            r'openlink\.php',
                            r'search.*\.php'
                        ]
                        
                        has_api_info = False
                        for pattern in api_patterns:
                            if re.search(pattern, js_response.text, re.IGNORECASE):
                                has_api_info = True
                                break
                        
                        if has_api_info:
                            logger.info(f"✓ JavaScript文件 {js_url} 可能包含API调用信息")
                            # 保存这个JavaScript文件进行进一步分析
                            filename = f'js_file_{i+1}.js'
                            with open(filename, 'w', encoding='utf-8') as f:
                                # 只保存前20000字符以避免过大文件
                                f.write(js_response.text[:20000] + '...')
                            logger.info(f"  JavaScript文件已保存到 {filename}")
                    
                except requests.exceptions.RequestException as e:
                    logger.error(f"✗ 获取JavaScript文件 {js_url} 时出错: {str(e)}")
            
            # 尝试模拟SPA应用可能的API请求格式
            logger.info("尝试模拟SPA应用可能的API请求...")
            
            # 基于常见的SPA API格式
            spa_api_patterns = [
                f'/api/search?q={quote(search_term)}',
                f'/api/v1/search?q={quote(search_term)}',
                f'/api/v2/search?q={quote(search_term)}',
                f'/search?q={quote(search_term)}',
                f'/api/books?q={quote(search_term)}',
                f'/api/v1/books?q={quote(search_term)}',
                f'/api/v2/books?q={quote(search_term)}',
                f'/opac/api/search?q={quote(search_term)}',
                f'/opac/api/v1/search?q={quote(search_term)}',
                f'/opac/api/v2/search?q={quote(search_term)}',
                
                # 尝试带有不同参数的请求
                f'/api/search?query={quote(search_term)}&page=1&limit=10',
                f'/api/books?query={quote(search_term)}&page=1&limit=10',
                f'/search?query={quote(search_term)}&page=1&limit=10',
                
                # 尝试POST请求
                f'/api/search',
                f'/api/v1/search',
                f'/api/v2/search',
                f'/search'
            ]
            
            # 测试GET请求
            for endpoint in spa_api_patterns:
                if endpoint.lower() != '/search':  # 跳过POST请求的模式
                    full_url = urljoin(self.base_url, endpoint)
                    logger.info(f"测试GET请求: {full_url}")
                    
                    try:
                        response = self.session.get(full_url, timeout=15)
                        if response.status_code == 200:
                            # 检查是否为JSON
                            try:
                                json_data = response.json()
                                logger.info(f"✓ GET请求 {full_url} 返回有效的JSON数据")
                                logger.info(f"  JSON数据结构: {list(json_data.keys()) if isinstance(json_data, dict) else f'数组长度: {len(json_data)}'}")
                                
                                # 保存JSON数据
                                filename = f'spa_api_response_{endpoint.replace("/", "_")}.json'
                                with open(filename, 'w', encoding='utf-8') as f:
                                    f.write(response.text)
                                logger.info(f"  JSON数据已保存到 {filename}")
                                
                            except ValueError:
                                # 不是JSON，可能是HTML或其他格式
                                logger.info(f"✓ GET请求 {full_url} 返回非JSON数据，长度: {len(response.text)} 字符")
                        
                    except requests.exceptions.RequestException as e:
                        logger.error(f"✗ GET请求 {full_url} 失败: {str(e)}")
            
            # 测试POST请求
            post_endpoints = [
                f'/api/search',
                f'/api/v1/search',
                f'/api/v2/search',
                f'/search'
            ]
            
            for endpoint in post_endpoints:
                full_url = urljoin(self.base_url, endpoint)
                logger.info(f"测试POST请求: {full_url}")
                
                try:
                    # 尝试不同的请求体格式
                    post_data_options = [
                        {'query': search_term, 'page': 1, 'limit': 10},
                        {'q': search_term, 'page': 1, 'limit': 10},
                        {'keyword': search_term, 'page': 1, 'limit': 10},
                        {'strText': search_term, 'strSearchType': 'title'}
                    ]
                    
                    for i, post_data in enumerate(post_data_options):
                        logger.info(f"  测试POST数据格式 {i+1}/{len(post_data_options)}: {json.dumps(post_data)}")
                        response = self.session.post(full_url, json=post_data, timeout=15)
                        
                        if response.status_code == 200:
                            # 检查是否为JSON
                            try:
                                json_data = response.json()
                                logger.info(f"  ✓ POST请求返回有效的JSON数据")
                                logger.info(f"    JSON数据结构: {list(json_data.keys()) if isinstance(json_data, dict) else f'数组长度: {len(json_data)}'}")
                                
                                # 保存JSON数据
                                filename = f'spa_api_post_response_{endpoint.replace("/", "_")}_{i+1}.json'
                                with open(filename, 'w', encoding='utf-8') as f:
                                    f.write(response.text)
                                logger.info(f"    JSON数据已保存到 {filename}")
                                
                            except ValueError:
                                logger.info(f"  ✓ POST请求返回非JSON数据，长度: {len(response.text)} 字符")
                        
                except requests.exceptions.RequestException as e:
                    logger.error(f"✗ POST请求 {full_url} 失败: {str(e)}")
            
        except requests.exceptions.RequestException as e:
            logger.error(f"获取初始页面时出错: {str(e)}")
            return

if __name__ == "__main__":
    analyzer = SPAAnalyzer()
    analyzer.analyze_spa_search('Python')
    logger.info("SPA应用分析完成")