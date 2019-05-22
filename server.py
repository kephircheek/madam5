from flask import Flask, request, jsonify
import uuid
from requests import get
app = Flask(__name__)

@app.route('/home', methods=['GET'])
def hello_world():
    return 'Hello, World!\n\n'


@app.route('/submit', methods=['POST'])
def submit():
    if not request.form:
        return jsonify({'error':'Empty request'})

    elif 'url' not in request.form.keys():
        return jsonify({'error': 'Bad request: parametr (url) missing'})
    id = uuid.uuid4()
    while True:
        pass
    return jsonify({'id': str(id),
                    'url': request.form['url'],
                    'email': request.form.get('email', default = '...')})


@app.route('/check', methods=['GET'])
def check():
    if not request.args.keys():
        return jsonify({'error': 'Empty request'})
    elif 'id' not in request.args.keys():
        jsonify({'error': 'parameter (id) missing'})

    return jsonify('id', id)



if __name__ == '__main__':
    app.run(port=8000)

