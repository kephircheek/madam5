from flask import Flask, request, jsonify, make_response
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
        return make_response(jsonify({'error':'Empty request'}), 400)

    elif 'url' not in request.form.keys():
        return make_response(jsonify({'error': 'Bad request: parametr (url) missing'}), 400)

    uuid = str(uuid4())
    tasksDB.insert(uuid,
                   request.form['url'],
                   request.form.get('email'))

    t0 = time.time()
    r = q.enqueue_call(md5hasher, args=(uuid, request.form['url'], t0), result_ttl=86400)
    return make_response(jsonify({'id': uuid}), 200)

@app.route('/check', methods=['GET'])
def check():
    if not request.args.keys():
        return make_response(jsonify({'error': 'Empty request'}), 400)

    elif 'id' not in request.args.keys():
        return make_response(jsonify({'error': 'parameter (id) missing'}), 400)

    task = tasksDB.get(request.args['id'])
    if 'error' in task:
        return make_response(jsonify(task), 404)

    if task['status'] != 'done':
        return make_response(jsonify({'status': task['status']}), 200)

    return make_response(jsonify(task), 200)

@app.route('/history', methods=['GET'])
def history():
    return tasksDB.get_all()


if __name__ == '__main__':
    host = ''
    port = 8000
    app.run(host=host, port=port)

