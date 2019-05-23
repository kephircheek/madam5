import sqlite3
from uuid import uuid4

class TasksDB:
    def __init__(self):
        self.conn = sqlite3.connect('tasks.db', check_same_thread=False)
        cursor = self.conn.cursor()
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS tasks
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                           uuid CHAR(36),
                           rid INTEGER NOT NULL,
                           url VARCHAR(255),
                           email VARCHAR(255),
                           status VARCHAR(255),
                           md5 VARBINARY(4194304))''') # < 4 Mb
        cursor.close()
        self.conn.commit()

    def insert(self, rid, url, email=''):
        status = 'running'
        uuid = str(uuid4())
        cursor = self.conn.cursor()
        cursor.execute('''INSERT INTO tasks
                          (uuid, rid, url, email, status)
                          VALUES (?, ?, ?, ?, ?)''',
                          (uuid, rid, url, email, 'running'))
        cursor.close()
        self.conn.commit()
        return uuid

    def get(self, uuid):
        cursor = self.conn.cursor()
        row = cursor.execute('SELECT * FROM tasks WHERE uuid = ?', (uuid,))
        row = cursor.fetchone()
        return {'uuid': row[1],
                'rid': row[2],
                'url': row[3],
                'email': row[4],
                'status': row[5],
                'md5': row[6]}

    def get_all(self):
        cursor = self.conn.cursor()
        rows = cursor.execute('SELECT * FROM tasks')
        rows = cursor.fetchall()
        return '\n'.join([' | '.join(map(str, line)) for line in rows]) + '\n\n'
