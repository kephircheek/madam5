# madam5
Madam5 - веб сервис для вычисления [**MD5 hash**](https://ru.wikipedia.org/wiki/MD5) от файла расположеного в сети Интернет. 

---

## Установка
1. [**Redis**](https://redis.io/topics/quickstart) - хранилище данных и брокер сообщений
```
wget http://download.redis.io/redis-stable.tar.gz
tar xvzf redis-stable.tar.gz
cd redis-stable
make
```

В MacOS можно так
```
brew install redis
```

2. [**RQ**](https://python-rq.org) - простая очередь для Redis  
3. [**FLask**](http://flask.pocoo.org) 
```
pip install -r requirements.txt
```

## Запуск

1. Запускаем Redis
```
redis-server
```
2. Запускаем рабочий процесс(можно создать несколько рабочих процессов)
```
rq worker
```
3. Запускаем приложение `server.py` (по умолчанию: `host=localhost`, `port=8000`)
```
python server.py
```

## полезные ссылочки
[Flask -> request](http://flask.pocoo.org/docs/0.12/api/?highlight=request#flask.request)

[MD5_hash in python](https://stackoverflow.com/questions/49958006/python-3-create-md5-hash)

[Flask + RQ](https://habr.com/en/post/307140/)

[SQL](https://www.w3schools.com/sql/sql_datatypes.asp)
