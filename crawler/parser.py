from typing import List
from bs4 import BeautifulSoup
from crawler.models import Collection, Book, BookList, Record
class NJULibParser:
    def brief_parser(self, html: str) -> BookList:
        soup = BeautifulSoup(html, 'lxml')
        results = soup.find_all('a', class_='weui-media-box weui-media-box_appmsg')
        book_list: BookList = BookList()
        for result in results:
            detail_url = result['href']
            title = result.find('h4', class_='weui-media-box__title').text.strip()
            author = result.find_all('p', class_='weui-media-box__desc')[0].text.strip()[4:]
            isbn = result.find_all('p', class_='weui-media-box__desc')[1].text.strip()
            publication_info = result.find_all('p', class_='weui-media-box__desc')[2].text.strip()[5:]
            book = Book(title, author, isbn, publication_info, detail_url)
            book_list.add_book(book, merge = False)
        return book_list

    def detail_parser(self, html: str) -> Collection:
        collection: Collection = Collection()
        detail_soup = BeautifulSoup(html, 'lxml')
        loc_items = detail_soup.find_all('div', class_='loc_item')
        for loc_item in loc_items:
            location = loc_item.find('b').text.split()[0].strip()
            borrow_status = loc_item.find('b').text.split()[2].strip().strip('—').strip('-')
            book_status = loc_item.find('span', class_='tag').text.strip()
            call_num = loc_item.find('p', class_='loc_info').text.replace(' ', '').split('|')[0].strip()
            code_num = loc_item.find('p', class_='loc_info').text.replace(' ', '').split('|')[1].strip()
            edition = loc_item.find('p', class_='loc_info').text.replace(' ', '').split('|')[2].strip().strip('-')
            #abstract_list = detail_soup.find('div', class_='middle_info').text.split()
            #abstract = ' '.join(abstract_list[1:])
            new_record = Record(location)
            new_record.add_copy(borrow_status, book_status, call_num, code_num, edition)
            collection.add_record(new_record)
        return collection