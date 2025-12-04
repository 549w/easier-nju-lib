from opac_spider import OPACSpider

# 初始化爬虫
spider = OPACSpider()

# 搜索图书
books = spider.search_books_by_title('Python', max_results=5)

# 打印结果
print(f'获取到 {len(books)} 本图书')
for book in books:
    print(f"书名: {book['title']}, 作者: {book['author']}")