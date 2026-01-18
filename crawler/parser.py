from typing import List
from bs4 import BeautifulSoup
from crawler.models import Collection, Book, BookList
from exceptions import ParseError
class NJULibParser:
    def brief_parser(self, html: str) -> BookList:
        soup = BeautifulSoup(html, 'lxml')
        results = soup.find_all('a', class_='weui-media-box weui-media-box_appmsg')
        book_list: BookList = BookList()
        for result in results:
            detail_url = result['href']
            if detail_url is None:
                raise ParseError('detail_url is not found')
            title = result.find('h4', class_='weui-media-box__title').text.strip()
            if title is None:
                raise ParseError('title is not found')
            details = result.find_all('p', class_='weui-media-box__desc')
            if len(details) < 3:
                raise ParseError('details are not complete')
            author = result.find_all('p', class_='weui-media-box__desc')[0].text.strip()
            isbn = result.find_all('p', class_='weui-media-box__desc')[1].text.strip()
            publication_info = result.find_all('p', class_='weui-media-box__desc')[2].text.strip()
            book = Book(title, author, isbn, publication_info, detail_url)
            book_list.add_book(book, merge = False)
        return book_list

    def detail_parser(self, html: str) -> Collection:
        collection = Collection()
        detail_soup = BeautifulSoup(html, 'lxml')
        loc_items = detail_soup.find_all('div', class_='loc_item')
        for loc_item in loc_items:
            place_info_node = loc_item.find('b')
            if place_info_node is None:
                raise ParseError('loc info node is not found')
            location = place_info_node.text.split()[0]
            borrow_status = place_info_node.text.split()[2]
            book_status_node = loc_item.find('span', class_='tag')
            if book_status_node is None:
                raise ParseError('book status node is not found')
            book_status = book_status_node.text
            loc_info_node = loc_item.find('p', class_='loc_info')
            if loc_info_node is None:
                raise ParseError('loc info node is not found')
            call_num = loc_info_node.text.split()[0]
            code_num = loc_info_node.text.split()[2]
            #abstract_list = detail_soup.find('div', class_='middle_info').text.split()
            #abstract = ' '.join(abstract_list[1:])
            collection.add_record(location, borrow_status, book_status, call_num, code_num)
        return collection