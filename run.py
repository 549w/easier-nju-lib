from config.settings import NAMES_TO_CAMPUSES
from crawler.service import NJULibService

from flask import Flask, request, jsonify

app = Flask(__name__)
app.json.ensure_ascii = False

model_post = {
    'keyword' : '',#required
    'max_num_of_results' : 10,#optional
    'name_selected' : '',#optional
    'author': '',#optional
    'press': ''#optional
}

def bad_request(message: str):
    return {
        'code': 400,
        'message': message
    }, 400

@app.route('/api/search', methods = ['POST'])

def search():

    keyword = request.json.get('keyword')
    if keyword is None:
        return bad_request('Missing keyword')
    keyword: str = str(keyword).strip()
    if keyword == '':
        return bad_request('Keyword cannot be empty')

    max_num_of_results = request.json.get('max_num_of_results')
    if max_num_of_results is None:
        max_num_of_results: int = 15
    elif not isinstance(max_num_of_results, int):
        return bad_request('Wrong type of max_num_of_results')
    else:
        max_num_of_results: int = int(max_num_of_results)
        if max_num_of_results < 10 or max_num_of_results > 100:
            return bad_request('max_num_of_results must be between 10 and 100')

    name_selected = request.json.get('name_selected')
    author = request.json.get('author')
    press = request.json.get('press')
    books = NJULibService().search(keyword, max_num_of_results)

    if name_selected:
        campus_selected = NAMES_TO_CAMPUSES[str(name_selected)]
        books = NJULibService().sort_by_campus(books, campus_selected)
    if author:
        books.sort_by_author(str(author).strip())
    if press:
        books.sort_by_press(str(press).strip())

    return books.to_dict()

if __name__ == '__main__':
    app.run(host="localhost", port=5000)