from flask import Flask, jsonify
app = Flask(__name__)

@app.route('/test', methods=['GET'])
def test():
    return jsonify({'message': '测试成功', 'data': [1, 2, 3]})

if __name__ == '__main__':
    app.run(port=5001, debug=True)