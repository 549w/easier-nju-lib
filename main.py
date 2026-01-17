import streamlit as st
from config.settings import NAMES_TO_CAMPUSES, STATUS_DISPLAY
from crawler.service import NJULibService
from annotated_text import annotated_text

st.title('Easier NJU Lib - 更好用的NJU图书馆检索方式')

campuses: list = NAMES_TO_CAMPUSES.keys()
name_selected = st.segmented_control(
    "校区", campuses, selection_mode="single"
)
if name_selected:
    campus_selected = NAMES_TO_CAMPUSES[name_selected]
max_num_of_results = st.slider("最大搜索条数", 10, 100, 15)
keyword = st.text_input('书名').strip()
press = st.text_input('出版社（可选）').strip()
if st.button("搜索"):
    #st.write(f'{campus_selected} hello, {keyword}')
    if keyword:
        with st.spinner('正在搜索……', show_time = True):
            books = NJULibService().search(keyword, max_num_of_results)
            if name_selected:
                books = NJULibService().sort_by_campus(books, campus_selected)
            if press:
                books.sort_by_press(press)
        if len(books.list) == 0:
            st.warning('未搜索到任何结果。')
        else:
            st.success('搜索完成！')
            st.balloons()
        for book in books.list:
            with st.container(border=True):
                st.header(book.title)
                st.markdown(f':grey-badge[:material/person: {book.author}] :grey-badge[:material/house: {book.publication_info}]')
                if len(book.collection.list) == 0:
                    st.warning('这本书没有馆藏信息。')
                for record in book.collection.list:
                    record.sort_copies()
                    with st.container(border=True, gap = None):
                        st.markdown(f':violet-badge[:material/location_on: {record.location}]')
                        #st.write(record.location)
                        for copy in record.copies:
                            message: str = f""
                            if copy.borrow_status in STATUS_DISPLAY.keys():
                                message += f"{STATUS_DISPLAY[copy.borrow_status]}"
                            else:
                                message += f"{copy.borrow_status}"
                            if copy.book_status in STATUS_DISPLAY.keys():
                                message += f"{STATUS_DISPLAY[copy.book_status]}"
                            #elif copy.book_status == ''
                            else:
                                message += f"{copy.book_status}"
                            message += f"{copy.call_num} {copy.code_num}"

                            message += f"{copy.edition}"
                            st.markdown(message)
    else:
        st.warning('请输入书名。')