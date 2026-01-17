from flask import Flask
from flask import request
from flask import make_response
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[1]))
app = Flask(__name__)

@app.route('/')

def home():
    return 'home'

@app.route('/test')

def test():
    return 'test'

@app.route('/search/<keyword>')
def search(keyword: str):
    return f'searching {keyword}'


if __name__ == '__main__':
    app.run(debug=True)