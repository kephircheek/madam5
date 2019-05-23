# madam5
Madam5 - веб сервис на `Python3` для вычисления [**MD5 hash**](https://ru.wikipedia.org/wiki/MD5) от файла расположеного в сети Интернет. 

---
Сервер написан на `python3` с помощью `[Flask](http://flask.pocoo.org)`. 
Скачивание файла и подсчет hash происходит в фоновом режиме благодаря `[Redis](https://redis.io/topics/quickstart)`.



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
3. [**FLask**](http://flask.pocoo.org) - фреймворк для создания веб-приложений
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

## Функциональность 

### POST
Запрос на обраоку файла делается через форму с одним обязательным полем `url` (поле `email` необязательное). Пример:
```
curl -X POST -d "url=http://mysite.com/myfile.data" http://localhost:8000/submit
```
Или
```
curl -X POST -d "email=myemail@mailbox.com&url=http://mysite.com/myfile.data" http://localhost:8000/submit
```
В ответ сервер выдает `uuid` запроса. Пример:

Запрос
```
curl -X POST -d "url=http://link" http://localhost:8000/submit
```
Ответ:
```
{"id":"22b16fc8-3a4b-4a8e-aa88-e65bb57b3358"}
```
## GET 

### check
Запрос на получение статуса запроса можно сделать с помощью `uuid`
```
curl -X GET http://localhost:8000/check?id=22b16fc8-3a4b-4a8e-aa88-e65bb57b3358
```
Пример ответа сервера:
```
{"status":"request error"}
```
Это значит в запросе была передана плохая ссылка ~~(ошибка `requests.get()`)~~.

Если ссылка правильная:
Запрос:
```
curl -X POST -d "url=https://i.ytimg.com/vi/r4OiHPWpNxU/maxresdefault.jpg" http://localhost:8000/submit
```
Ответ:
```
{"id":"2e1b5cd5-121e-455e-a56e-335fa1902122"}
```
Запрос:
```
curl -X GET http://localhost:8000/check?id=2e1b5cd5-121e-455e-a56e-335fa1902122
```
Пример ответа сервера:
```
{"email":null,"md5":"c115069008b18a79ff03e8c9256e5161","status":"done","url":"https://i.ytimg.com/vi/r4OiHPWpNxU/maxresdefault.jpg","uuid":"2e1b5cd5-121e-455e-a56e-335fa1902122"}
```
Также сервер может ответить:
```
{"status":"running"}
```
Это занчит, что запрос в очереди или выполняется. 


### history 
Историю всех запросов можно посмотреть с помощь запроса 
```
curl -X GET http://localhost:8000/history
```

## полезные ссылки
* [Flask + Redis](https://habr.com/en/post/307140/)
* [Flask -> request](http://flask.pocoo.org/docs/0.12/api/?highlight=request#flask.request)
* [MD5_hash in python](https://stackoverflow.com/questions/49958006/python-3-create-md5-hash)
* [SQL](https://www.w3schools.com/sql/sql_datatypes.asp)
