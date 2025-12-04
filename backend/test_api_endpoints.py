import requests
import logging
import time
from urllib.parse import urljoin

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('API_Tester')

class APITester:
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
    
    def test_api_endpoints(self, search_term):
        """测试各种可能的API端点"""
        logger.info(f"开始测试API端点，搜索词: {search_term}")
        
        # 常见的图书馆OPAC API端点格式
        api_endpoints = [
            # 标准OPAC API格式
            f'/api/search?query={search_term}',
            f'/opac/api/search?query={search_term}',
            f'/api/opac/search?query={search_term}',
            
            # 基于CIRSS的系统
            f'/opac/search.php?q={search_term}',
            f'/opac/ajax_search.php?q={search_term}',
            f'/opac/json_search.php?q={search_term}',
            
            # 可能的REST API格式
            f'/api/v1/books/search?term={search_term}',
            f'/api/v2/books/search?query={search_term}',
            
            # 尝试与原搜索页面相似的参数
            f'/opac/openlink.php?strSearchType=title&match_flag=forward&strText={search_term}&doctype=ALL&page=1&format=json',
            f'/opac/openlink.php?strSearchType=title&match_flag=forward&strText={search_term}&doctype=ALL&page=1&output=json',
            f'/opac/openlink.php?strSearchType=title&match_flag=forward&strText={search_term}&doctype=ALL&page=1&type=json',
            
            # 尝试其他搜索参数组合
            f'/opac/openlink.php?strSearchType=title&strText={search_term}&page=1',
            f'/opac/openlink.php?strSearchType=title&strText={search_term}&doctype=ALL',
            
            # 尝试直接访问静态资源
            f'/static/api/books.json',
            f'/data/books.json'
        ]
        
        # 测试每个API端点
        for i, endpoint in enumerate(api_endpoints):
            full_url = urljoin(self.base_url, endpoint)
            logger.info(f"测试端点 {i+1}/{len(api_endpoints)}: {full_url}")
            
            try:
                response = self.session.get(full_url, timeout=15)
                
                # 检查响应
                if response.status_code == 200:
                    # 检查是否为JSON
                    try:
                        json_data = response.json()
                        logger.info(f"✓ 端点 {full_url} 返回有效的JSON数据")
                        logger.info(f"  JSON数据结构: {list(json_data.keys()) if isinstance(json_data, dict) else f'数组长度: {len(json_data)}'}")
                        
                        # 保存JSON数据
                        with open(f'api_response_{i+1}.json', 'w', encoding='utf-8') as f:
                            f.write(response.text)
                        logger.info(f"  JSON数据已保存到 api_response_{i+1}.json")
                        
                    except ValueError:
                        # 不是JSON，检查是否为XML或其他格式
                        content_type = response.headers.get('Content-Type', '')
                        logger.info(f"✓ 端点 {full_url} 返回数据，内容类型: {content_type}")
                        logger.info(f"  响应长度: {len(response.text)} 字符")
                        
                        # 保存响应内容
                        with open(f'api_response_{i+1}.txt', 'w', encoding='utf-8') as f:
                            f.write(response.text[:1000] + '...')  # 只保存前1000个字符
                        logger.info(f"  响应内容(前1000字符)已保存到 api_response_{i+1}.txt")
                else:
                    logger.warning(f"✗ 端点 {full_url} 返回错误状态码: {response.status_code}")
                    
            except requests.exceptions.RequestException as e:
                logger.error(f"✗ 访问端点 {full_url} 时出错: {str(e)}")
            
            # 避免过于频繁的请求
            time.sleep(1)
        
        logger.info("所有API端点测试完成")

if __name__ == "__main__":
    tester = APITester()
    tester.test_api_endpoints('Python')
    logger.info("测试完成")