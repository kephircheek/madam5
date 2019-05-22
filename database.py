import sqlite3

class TasksDB:
    def __init__(self):
        self.conn = sqlite3.connect('tasks.db', check_same_thread=False)
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS tasks
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                           uuid CHAR(36),
                           rid INTEGER NOT NULL,
                           url VARCHAR(255),
                           email VARCHAR(255))''')
        cursor.close()
        self.conn.commit()

    def insert(self, uuid, rid, url, email=''):
        cursor = self.conn.cursor()
        cursor.execute('''INSERT INTO tasks
                          (uuid, rid, url, email)
                          VALUES (?, ?, ?, ?)''', (uuid, rid, url, email))
        cursor.close()
        self.conn.commit()

    def get(self, uuid):
        cursor = self.conn.cursor()
        row = cursor.execute('SELECT * FROM tasks WHERE uuid = ?', (uuid,))
        row = cursor.fetchone()
        return row

    def get_all(self):
        cursor = self.conn.cursor()
        rows = cursor.execute('SELECT * FROM tasks')
        rows = cursor.fetchall()
        return rows
