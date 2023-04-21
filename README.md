# api_yamdb

## _Описание проекта_

Проект API системы сбора отзывов и на различные произведения (кино, музыка, фильмы, книги)

## Доступный функционал

- Для аутентификации используются JWT-токены.
- У неаутентифицированных пользователей доступ к API только на уровне чтения.
- Создание объектов разрешено только аутентифицированным пользователям.На прочий фунционал наложено ограничение в виде административных ролей и авторства.
- Управление пользователями.
- Получение списка всех категорий и жанров, добавление и удаление.
- Получение списка всех произведений, их добавление.Получение, обновление и удаление конкретного произведения.
- Получение списка всех отзывов, их добавление.Получение, обновление и удаление конкретного отзыва.  
- Получение списка всех комментариев, их добавление.Получение, обновление и удаление конкретного комментария.
- Возможность получения подробной информации о себе и удаления своего аккаунта.
- Фильтрация по полям.

### Документация к API доступна по адресу [http://127.0.0.1:8000/redoc/](http://127.0.0.1:8000/redoc/) после запуска сервера с проектом

## Технологии

- Python 3.9
- Django
- Django Rest Framework
- Simple JWT
- SQLite3

## _Как запустить проект_:

Клонировать репозиторий на локальную машину:

git clone https://github.com/Adelina1231/api_yamdb.git

Cоздать и активировать виртуальное окружение:

```
python3 -m venv env
```

* Если у вас Linux/macOS

    ```
    source env/bin/activate
    ```

* Если у вас windows

    ```
    source env/scripts/activate
    ```

```
python3 -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```
## Импорт данных из csv-файла в базу данных

Код для импорта тестовой базы данных находится в файле: “api_yamdb\reviews\management\commands\import_csv.py”

Импорт базы данных осуществляется командой:

“python manage.py import_csv”

(Импорт необходимо осуществлять на чистую БД).

При наличии ошибок при импорте, необходимо сбросить все миграции и выполнить их повторно.

## Алгоритм регистрации пользователей
- Пользователь отправляет запрос с параметрами *email* и *username* на */auth/signup/*.
- YaMDB отправляет письмо с кодом подтверждения (confirmation_code) на указаный *email* .
- Пользователь отправляет запрос с параметрами *email* и *confirmation_code* на */auth/token/*, в ответе на запрос ему приходит token (JWT-токен).

## Пользовательские роли
**Аноним** — может просматривать описания произведений, читать отзывы и комментарии.

**Аутентифицированный пользователь (user)** — может читать всё, как и Аноним, дополнительно может публиковать отзывы и ставить рейтинг произведениям (фильмам/книгам/песенкам), может комментировать чужие отзывы и ставить им оценки; может редактировать и удалять свои отзывы и комментарии.

**Модератор (moderator)** — те же права, что и у Аутентифицированного пользователя плюс право удалять и редактировать любые отзывы и комментарии.

**Администратор (admin)** — полные права на управление проектом и всем его содержимым. Может создавать и удалять произведения, категории и жанры. Может назначать роли пользователям.

**Администратор Django** — те же права, что и у роли Администратор.

## Набор доступных эндпоинтов:
* ```redoc/``` - Подробная документация по работе API.
* ```api/v1/categories/``` - Получение, публикация и удаление категорий (_GET, POST, DELETE_).
* ```api/v1/genres/``` - Получение, публикация и удаление жанров (_GET, POST, DELETE_).
* ```api/v1/titles/``` - Получение и публикация произведения (_GET, POST_).
* ```api/v1/titles/{id}``` - Получение, изменение, удаление произведения с соответствующим **id** (_GET, PUT, PATCH, DELETE_).
* ```api/v1/titles/{title_id}/reviews/``` - Получение отзывов к произведению с соответствующим **title_id** и публикация новых отзывов(_GET, POST_).
* ```api/v1/titles/{title_id}/reviews/{id}/``` - Получение, изменение, удаление отзыва с соответствующим **id** к произведению с соответствующим **title_id** (_GET, PUT, PATCH, DELETE_).
*  ```api/v1/titles/{title_id}/reviews/{review_id}/comments/``` -  Получение комменатриев и публикация нового комментария к отзыву с соответствующим **review_id**, при этом отзыв оставлен к произведению с соответствующим **title_id**(_GET, POST_).
*  ```api/v1/titles/{title_id}/reviews/{review_id}/comments/{id}/``` -  Получение, изменение, удаление комменатрия с соответствующим **id** к отзыву с соответствующим **review_id**, при этом отзыв оставлен к произведению с соответствующим **title_id** (_GET, PUT, PATCH, DELETE_).

## _Примеры выполнения запросов_:
##### Получаем JWT-токена 
>```api/v1/auth/token/```
>
>Payload
>```json
>{
>"username": "string",
>"confirmation_code": "string"
>}
>```
>Response sample (status code = 200)
>```json
>{
>"token": "string"
>}
>```


##### Получение списка всех произведений 
>```api/v1/titles/```
>
>Response sample (status code = 200)
>```json
>[
>  {
>    "count": 0,
>    "next": "string",
>    "previous": "string",
>    "results": [
>      {
>        "id": 0,
>        "name": "string",
>        "year": 0,
>        "rating": 0,
>        "description": "string",
>        "genre": [
>          {
>            "name": "string",
>            "slug": "string"
>          }
>        ],
>        "category": {
>          "name": "string",
>          "slug": "string"
>        }
>      }
>    ]
>  }
>]
>```


##### Опубликовать новый отзыв. 
(*требуется Аутентификация*)
>```api/v1/titles/{title_id}/reviews/```
>
>Payload
>```json
>{
>"text": "string",
>"score": 1
>}
>```
>Response sample (status code = 201)
>```json
>{
>"id": 0,
>"text": "string",
>"author": "string",
>"score": 1,
>"pub_date": "2019-08-24T14:15:22Z"
>}
>```
## Авторы проекта
Аделина Тазиева - [https://github.com/Adelina1231](https://github.com/Adelina1231)     
Екатерина Казина - [https://github.com/KateKazino](https://github.com/KateKazino)   
Лариса Дербасова - [https://github.com/mielik](https://github.com/mielik)
