import requests
from Tools.scripts.var_access_benchmark import loop_overhead
from bs4 import BeautifulSoup
import re

class SearchResult:

    def __init__(self, url, title, author, ISBN, publication_info):
        self.url = url
        self.title = title
        self.author = author
        self.ISBN = ISBN
        self.publication_info = publication_info

url = "http://weixin.libstar.cn/weixin/unify/search"
root_url = "http://weixin.libstar.cn"

params = {
    'mappingPath': 'njulib',
    'groupCode': 200027,
    'pubId': 1,
    'searchFieldContent': '非暴力沟通',
    'searchField': 'keyWord',
    'page': 1,
    'rows': 100
}

response = requests.get(url, params)
response.encoding = 'utf-8'
# print(response.text)
soup = BeautifulSoup(response.text, 'lxml')
title_tag = soup.find('title')
#if title_tag:
#    print(title_tag.get_text())
results = soup.find_all('a', class_= 'weui-media-box weui-media-box_appmsg')
#print(len(results))
#print(results[0]['href'])
book_url = results[0]['href']
#print(book_url)
book_title = results[0].find('h4', class_ = 'weui-media-box__title')
author = results[0].find_all('p', class_ = 'weui-media-box__desc')[0]
ISBN = results[0].find_all('p', class_ = 'weui-media-box__desc')[1]
publication_info = results[0].find_all('p', class_ = 'weui-media-box__desc')[2]


#print(results[2])
#print(book_title.text)
#print(author.text[4:])
#print(ISBN.text[5:])
#print(publication_info.text[5:])

detail_resp = requests.get(root_url + book_url)
detail_soup = BeautifulSoup(detail_resp.text, 'lxml')
loc_items = detail_soup.find_all('div', class_ = 'loc_item')
#print(len(loc_items))
loc_item = loc_items[0]
#print(loc_item)
place = loc_item.find('b').text.split()[0]
can_borrow = loc_item.find('b').text.split()[2]
status = loc_item.find('span', class_ = 'tag').text
call_num = loc_item.find('p', class_ = 'loc_info').text.split()[0]
code_num = loc_item.find('p', class_ = 'loc_info').text.split()[2]
abstract_list = detail_soup.find('div', class_ = 'middle_info').text.split()
abstract = ' '.join(abstract_list[1:])
#print(detail_soup.find('div', class_ = 'middle_info').text.split())

#print(abstract)
#print(repr(detail_soup.find('img')['src']))