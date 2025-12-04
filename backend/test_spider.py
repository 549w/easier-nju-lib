#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
直接测试OPACSpider类，不通过Flask应用
"""

import sys
from opac_spider import OPACSpider

# 设置日志级别为DEBUG以查看详细信息
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# 创建爬虫实例
print("创建爬虫实例...")
spider = OPACSpider()

# 直接调用搜索方法测试
print("\n调用search_books_by_title方法...")
query = "Python"
print(f"搜索关键词: {query}")

# 调用方法并打印结果
results = spider.search_books_by_title(query)
print(f"\n搜索结果数量: {len(results)}")
print("\n搜索结果详情:")
for i, book in enumerate(results, 1):
    print(f"\n图书 {i}:")
    for key, value in book.items():
        print(f"  {key}: {value}")

print("\n测试完成！")
