from flask import Flask, request, jsonify
from requests import get
from database import TasksDB
from uuid import uuid4

from redis import Redis
from rq import Queue

from tools import md5hasher

import time

app = Flask(__name__)
tasksDB = TasksDB()

q = Queue(connection=Redis(), default_timeout=3600)


@app.route('/submit', methods=['POST'])
def submit():
    if not request.form:
        return jsonify({'error':'Empty request'})

    elif 'url' not in request.form.keys():
        return jsonify({'error': 'Bad request: parametr (url) missing'})

    uuid = str(uuid4())
    tasksDB.insert(uuid,
                   request.form['url'],
                   request.form.get('email'))

    t0 = time.time()
    r = q.enqueue_call(md5hasher, args=(uuid, request.form['url'], t0), result_ttl=86400)
    return jsonify({'id': uuid})

@app.route('/check', methods=['GET'])
def check():
    if not request.args.keys():
        return jsonify({'error': 'Empty request'})

    elif 'id' not in request.args.keys():
        jsonify({'error': 'parameter (id) missing'})

    task = tasksDB.get(request.args['id'])
    if 'error' in task:
        return jsonify(task)

    if task['status'] != 'done':
        return jsonify({'status': task['status']})

    return jsonify(task)

@app.route('/history', methods=['GET'])
def history():
    return tasksDB.get_all()


if __name__ == '__main__':
    host = ''
    port = 8000
    app.run(host=host, port=port)

