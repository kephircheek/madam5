import sqlite3

class TasksDB:
    def __init__(self):
        self.conn = sqlite3.connect('tasks.db', check_same_thread=False)
        cursor = self.conn.cursor()
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS tasks
                           (id INTEGER PRIMARY KEY AUTOINCREMENT,
                           uuid CHAR(36),
                           url VARCHAR(255),
                           email VARCHAR(255),
                           status VARCHAR(255),
                           time INTEGER,
                           md5 VARCHAR(32))''')
        cursor.close()
        self.conn.commit()

    def insert(self, uuid, url, email=''):
        status = 'running'
        cursor = self.conn.cursor()
        cursor.execute('''INSERT INTO tasks
                          (uuid, url, email, status)
                          VALUES (?, ?, ?, ?)''',
                          (uuid, url, email, 'running'))
        cursor.close()
        self.conn.commit()

    def update(self, uuid, status, time, md5=''):
        cursor = self.conn.cursor()
        cursor.execute('''UPDATE tasks
                          SET status = ?, time = ?, md5 = ?
                          WHERE uuid = ?''',
                          (status, time, md5, uuid))
        cursor.close()
        self.conn.commit()

    def get(self, uuid):
        cursor = self.conn.cursor()
        row = cursor.execute('SELECT * FROM tasks WHERE uuid = ?', (uuid,))
        row = cursor.fetchone()
        if not row:
            return {'error': f'task not exist with uuid: {uuid}'}

        return {'uuid': row[1],
                'url': row[2],
                'email': row[3],
                'status': row[4],
                'md5': row[6]}

    def get_all(self):
        cursor = self.conn.cursor()
        rows = cursor.execute('SELECT * FROM tasks')
        rows = cursor.fetchall()
        table = '\n'.join(['{:^2} | {:^36} | {:^40.40} | {:^30} | {:^14} | {:^6} | {:^32}'.format(
                           *['ID',  'UUID',   'URL', 'EMAIL', 'STATUS', 'TIME', 'MD5'])] +
                          ['{:^2} | {:^36} | {:^40.40} | {:^30} | {:^14} | {:^6} | {:^32}'.format(
                           *map(str, row)) for row in rows]) + '\n\n'
        return table
