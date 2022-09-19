# Проект YaMDb #
![Yamdb Status](https://github.com/themasterid/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg?branch=master&event=push)

#### Проект YaMDb представляет из себя хранилище информации о произведений различных категорий и жанров, отзывов пользователей и комментариев к ним. 

## Реализация проекта
Для реализации проекта выполнено написание бэкенда (приложение reviews) и API для него (приложение api) в соответствии с приложенной документацией API, содержащей информацию о возможных запросах и правах пользователей.

Документация API доступна по адресу http://127.0.0.1:8000/redoc/ при запущенном проекте.

### Ресурсы проекта: 
- Ресурс auth: аутентификация;
- Ресурс users: пользователи;
- Ресурс titles: произведения, к которым пишут отзывы (определённый фильм, книга или песенка);
- Ресурс categories: категории (типы) произведений («Фильмы», «Книги», «Музыка»);
- Ресурс genres: жанры произведений. Одно произведение может быть привязано к нескольким жанрам;
- Ресурс reviews: отзывы на произведения. Отзыв привязан к определённому произведению;
- Ресурс comments: комментарии к отзывам. Комментарий привязан к определённому отзыву.

### Технологии в проекте
Проект создается с использованием следующих технологий:
- Python 3.7;
- Django 2.2.16;
- Django-filter 21.1;
- Djangorestframework 3.12.4;
- Djangorestframework-simplejwt 5.2.0;
- PyJWT 2.1.0.
- gunicorn==20.0.4
- psycopg2-binary==2.8.6

### Инструкции по запуску
- Установите и активируйте виртуальное окружение
- Установите зависимости из файла requirements.txt
```
pip install -r requirements.txt
``` 
- Для предварительной загрузки в базу данных подготовленных тестовых данных в папке с файлом manage.py выполните команду:
```
python manage.py load_data
```
- Для запуска проекта выполните команду в вышеуказанной папке:
```
python3 manage.py runserver
```
Обратите внимание, что загрузка тестовых данных не является обязательной и необходима для проверки работоспособности проекта без предварительного ручного заполнения базы данных.

### Инструкции по запуску в контейнерах
- Перейдите в папку /INFRA_SP2/infra
- Создайте файл с переменными окружения .env и заполните его по примеру:
```
DB_ENGINE= # указываем, c какой БД будем работать, например django.db.backends.postgresql
DB_NAME=default # имя базы данных
POSTGRES_USER=default # логин для подключения к базе данных
POSTGRES_PASSWORD=default # пароль для подключения к БД (установите свой)
DB_HOST=default # название сервиса (контейнера)
DB_PORT=default # порт для подключения к БД
SECRET_KEY=default
```
- Запускам Docker-compose:
```
docker-compose up -d
```
- Применяем миграции, создаем суперпользователя, собираем статику (выполнить поочередно):
```
docker-compose exec web python manage.py migrate

docker-compose exec web python manage.py createsuperuser

docker-compose exec web python manage.py collectstatic --no-input
```

Готово. Админка проекта будет доступна по адресу http://localhost/admin/

### Есть возможность заполнить БД начальными данными из файла
```
docker-compose exec web python manage.py load_data
```
Внимание! После массового импорта данных в БД происходит рассинхронизация
последовательности первичных ключей (primary key). Для исправления, необходимо
указать следующую последовательность вручную. Для это необходимо проделать следующее:
Подключится к postgres:
```
docker-compose exec db psql -U <example_username> -d <example_password>
```
<example_username> - user указанный в .env POSTGRES_USER
<example_password> - password указанный в .env POSTGRES_PASSWORD

Далее проверям максимальное значение ID в таблице reviews_review и
текущее значение последовательности (выполнить поочередно):
```
select max(id) from reviews_review;
select nextval('"reviews_review_id_seq"');
```
Убеждаемся, что первое значение больше второго. Задаем значение
для следующего числа последовательности:
```
select setval('reviews_review_id_seq', (select max(id) from reviews_review)+1);
```
Выходим из postgres:
```
exit
```

### Создать резервную копию БД
```
docker-compose exec web python manage.py dumpdata > fixtures.json
```

### Остновка/запуск готовых контейнеров
```
docker-compose stop
/
docker-compose start
```


## Авторы проекта
#### Cтуденты Яндекс.Практикума. Факультет: Разработчик Python. Когорта № 34. Команда № 26.

Дмитрий ExpertNSK Казаков - Teamlead, реализация ресурсов Auth и User, сборка проекта.  
Дмитрий kissboing Николаев - реализация ресурсов Categories, Genres и Titles.  
Станислав StKensirov Руцкий - реализация ресурсов Review и Comments, а также рейтинга произведений (Titles).  

MIT License

Copyright (c) 2022

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
