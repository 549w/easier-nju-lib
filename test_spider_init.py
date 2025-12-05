#!/usr/bin/env python3
# 极简的RealSpider初始化测试
import logging
import sys
import os

# 设置日志为DEBUG级别
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('TestSpiderInit')

try:
    logger.info("开始测试RealSpider初始化")
    
    # 添加backend目录到Python路径
    sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))
    
    # 直接测试OPACSpider
    logger.info("导入opac_spider...")
    from opac_spider import OPACSpider
    
    logger.info("创建OPACSpider实例...")
    opac_spider = OPACSpider()
    logger.info("OPACSpider实例创建成功！")
    
    # 测试RealSpider
    logger.info("导入RealSpider...")
    sys.path.append('.')
    from final_server import RealSpider
    
    logger.info("创建RealSpider实例...")
    real_spider = RealSpider()
    logger.info("RealSpider实例创建成功！")
    
    logger.info("测试搜索功能...")
    result = real_spider.search_books("Python")
    logger.info(f"搜索结果: {result}")
    
    logger.info("所有测试通过！")
    
except Exception as e:
    logger.critical(f"测试失败: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)