# Библиотека для доступа к микросервисам Платформы через API

## Использование

Установите библиотеку:
- `pip install git+https://github.com/syeysk/sy_api.git`

Для доступа к микросервисам необходим токен, получить который можно на странице "Токены для API":
<p align="center"><img src="getting_token_item.png" align="middle" width="65%"></p>

Для каждого микросервиса - отдельный токен.

## Микросервис заметок

Пример кода:
```python
from syapi.note import Note

token = 'here-your-token'
note = Note(token)

title = 'Заметка для теста'
content = 'а это её содержимое))'
note.create(title, content)
print(note.get(title))
new_title = 'Заметка для теста (обновлён заголовок)'
note.update(title, new_title=new_title)
note.update(new_title, new_content='ну вот и содержимое обновилось')
print(note.get(new_title))
note.delete(new_title)
```

Пример выведет следующее:
```plain
{'title': 'Заметка для теста', 'content': 'а это её содержимое))', 'source': 'default'}
{'title': 'Заметка для теста (обновлён заголовок)', 'content': 'ну вот и содержимое обновилось', 'source': 'default'}
```

Методы `create`, `get`, `update`, `delete` могут принимать последний аргумент `source`.
Если не указан, то будет использовано свойство `Note.default_source`.

Свойства класса `Note`:
- `Note.default_source` - идентификатор базы по-умолчанию. Если равно `None` (по-умолчанию),
  то будет использована база, являющая по-умолчанию на сервере.
- `Note.url_microservice_note` - URL микросервиса заметок. По-умолчанию - `https://cachebrain.fun`.
  Переопределив это свойство, можно, например, делать запросы к локальной копии микросервиса.

## Микросервис авторизации

```python
from syapi.auth import User
```

Для получения доступа есть несколько способов.

Ручная авторизация:
```python
user = User()
# через имя пользователя и пароль
userdata = user.login(username, password)
# через регистрацию
userdata = user.registrate(username, password, email)
# через внешний сервис авторизации
userdata = user.login_or_registrate_by_extern()
```

Во всех трёх способах методы возвращают `userdata`, содержат поле `token` - токен, который используется для доступа к управлению пользователем.
Токен имеет срок жизни.

Если вы авторизовались ранее и сохранили токен и ключи, то получить доступ можно сразу:
```python
user = User(token, microservice_auth_id, auth_public_key, private_key, public_key)
```

После чего, можно управлять пользователем:
```python
# получить информацию о пользователе
user_data = user.get()
# редактировать информацию о пользователе
changed_fields = user.put(first_name='new first name')
# удалить пользователя
user_data = user.delete()
```

## План разработки библиотеки

- [Дорожная карта](ROADMAP.md)