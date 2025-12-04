import requests
import logging
import time
import re
from urllib.parse import urljoin, urlencode

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('NetworkAnalyzer')

class NetworkAnalyzer:
    def __init__(self):
        self.session = requests.Session()
        self.session.verify = False
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Referer': 'https://opac.nju.edu.cn/',
            'Connection': 'keep-alive'
        }
        
    def analyze_opac_search(self, search_term):
        """分析OPAC系统的搜索请求"""
        logger.info(f"开始分析OPAC搜索: {search_term}")
        
        # 基础URL
        base_url = 'https://opac.nju.edu.cn'
        search_url = f'{base_url}/opac/openlink.php'
        
        # 搜索参数
        search_params = {
            'strSearchType': 'title',
            'match_flag': 'forward',
            'strText': search_term,
            'doctype': 'ALL',
            'page': 1
        }
        
        # 发送搜索请求
        try:
            response = self.session.get(search_url, params=search_params, timeout=30)
            response.raise_for_status()
            logger.info(f"成功获取搜索页面，状态码: {response.status_code}")
            
            # 保存页面内容
            with open('opac_search.html', 'w', encoding='utf-8') as f:
                f.write(response.text)
            logger.info("搜索页面已保存到 opac_search.html")
            
            # 分析页面内容
            self._analyze_page_content(response.text)
            
        except Exception as e:
            logger.error(f"分析搜索页面时出错: {str(e)}")
            return None
    
    def _analyze_page_content(self, page_content):
        """分析页面内容，寻找API端点和数据"""
        logger.info("开始分析页面内容...")
        
        # 寻找可能的API端点
        api_patterns = [
            r'https?://[\w\.-]+/api/[\w/]+',
            r'\.api\.\w+',
            r'/api/[\w/]+',
            r'fetch\(["\']([^"\']+)["\']',
            r'axios\.(get|post|put|delete)\(["\']([^"\']+)["\']'
        ]
        
        found_apis = []
        for pattern in api_patterns:
            matches = re.findall(pattern, page_content)
            if matches:
                # 处理不同的匹配结果格式
                if isinstance(matches[0], tuple):
                    for match in matches:
                        if match[1]:
                            found_apis.append(match[1])
                else:
                    found_apis.extend(matches)
        
        if found_apis:
            logger.info(f"找到可能的API端点: {list(set(found_apis))}")
            with open('found_apis.txt', 'w', encoding='utf-8') as f:
                for api in list(set(found_apis)):
                    f.write(f"{api}\n")
        else:
            logger.info("未找到明显的API端点")
        
        # 寻找可能的数据结构
        data_patterns = [
            r'window\.([\w]+)\s*=\s*({[^}]+})',
            r'var\s+([\w]+)\s*=\s*({[^}]+})',
            r'const\s+([\w]+)\s*=\s*({[^}]+})',
            r'window\.([\w]+)\s*=\s*\[([^\]]+)\]',
            r'var\s+([\w]+)\s*=\s*\[([^\]]+)\]',
            r'const\s+([\w]+)\s*=\s*\[([^\]]+)\]'
        ]
        
        found_data = []
        for pattern in data_patterns:
            matches = re.findall(pattern, page_content, re.DOTALL)
            if matches:
                found_data.extend(matches)
        
        if found_data:
            logger.info(f"找到可能的数据结构: {len(found_data)} 个")
            with open('found_data.txt', 'w', encoding='utf-8') as f:
                for name, data in found_data:
                    f.write(f"变量名: {name}\n")
                    f.write(f"数据: {data[:200]}...\n\n")
        else:
            logger.info("未找到明显的数据结构")
        
        # 寻找script标签中的内容
        scripts = re.findall(r'<script[^>]*>(.*?)</script>', page_content, re.DOTALL)
        logger.info(f"找到 {len(scripts)} 个script标签")
        
        # 分析每个script标签
        for i, script_content in enumerate(scripts):
            if len(script_content) > 1000:  # 只分析较长的script标签
                logger.info(f"分析script标签 {i+1} (长度: {len(script_content)})")
                
                # 寻找可能的API调用
                api_calls = re.findall(r'\.ajax\([^)]+\)|fetch\([^)]+\)|axios\.[a-z]+\([^)]+\)', script_content)
                if api_calls:
                    logger.info(f"在script标签 {i+1} 中找到 {len(api_calls)} 个API调用")
                    with open(f'script_api_calls_{i+1}.txt', 'w', encoding='utf-8') as f:
                        for call in api_calls:
                            f.write(f"{call[:100]}...\n")

if __name__ == "__main__":
    analyzer = NetworkAnalyzer()
    analyzer.analyze_opac_search('Python')
    logger.info("分析完成")