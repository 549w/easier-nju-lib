from flask import Blueprint, request, render_template
from crawler.service import NJULibService
from crawler.models import BookList

search_bp = Blueprint(
    "search",
    __name__,
    url_prefix="/search"
)

@search_bp.route("", methods = ['GET'])

def search_page():
    keyword = request.args.get('keyword', "").strip()
    books: BookList = BookList()
    error: str|None = None
    if keyword:
        try:
            books = NJULibService().search(keyword)
        except Exception as e:
            error = str(e)
    return render_template(
        "search.html",
        keyword = keyword,
        books = books,
        error = error
    )