import time
import requests
from hashlib import md5
from database import TasksDB

def md5hasher(uuid, url, t0):
    '''t0 - time of adding task to queue in sec'''
    tasksDB = TasksDB()
    try:
        responce = requests.get(url)
    except requests.exceptions.RequestException as e:
        t = int(time.time() - t0)
        tasksDB.update(uuid=uuid, status=f'request error', time=t)
        return

    hash = md5(responce.content).hexdigest()
    t = int(time.time() - t0)
    tasksDB.update(uuid=uuid, status='done', time=t, md5=hash)

