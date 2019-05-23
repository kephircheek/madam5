from flask import Flask, request, jsonify
from requests import get
from database import TasksDB

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

    # add to queue
    rid = 1

    uuid = tasksDB.insert(rid,
                          request.form['url'],
                          request.form.get('email', default = '...'))

    return jsonify({'id': uuid})

@app.route('/check', methods=['GET'])
def check():
    if not request.args.keys():
        return jsonify({'error': 'Empty request'})

    elif 'id' not in request.args.keys():
        jsonify({'error': 'parameter (id) missing'})

    return jsonify(tasksDB.get(request.args['id']))

@app.route('/history', methods=['GET'])
def history():
    return tasksDB.get_all()


if __name__ == '__main__':
    app.run(port=8000)

