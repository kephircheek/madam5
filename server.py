from flask import Flask, request, jsonify
from requests import get
from database import TasksDB
import uuid

app = Flask(__name__)
tasksDB = TasksDB()

@app.route('/home', methods=['GET'])
def hello_world():
    return 'Hello, World!\n\n'


@app.route('/submit', methods=['POST'])
def submit():
    if not request.form:
        return jsonify({'error':'Empty request'})

    elif 'url' not in request.form.keys():
        return jsonify({'error': 'Bad request: parametr (url) missing'})
    id = str(uuid.uuid4())
    tasksDB.insert(id, 0, request.form['url'],
                   request.form.get('email', default = '...'))

    return jsonify({'id': id})

@app.route('/check', methods=['GET'])
def check():
    if not request.args.keys():
        return jsonify({'error': 'Empty request'})
    elif 'id' not in request.args.keys():
        jsonify({'error': 'parameter (id) missing'})
    row = tasksDB.get(request.args['id'])
    return ' | '.join(map(str, row)) + '\n\n'

@app.route('/history', methods=['GET'])
def history():
    return '\n'.join([' | '.join(map(str, line)) for line in tasksDB.get_all()]) + '\n\n'


if __name__ == '__main__':
    app.run(port=8000)

