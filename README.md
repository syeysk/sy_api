# Библиотека для доступа к микросервисам Платформы через API

## Использование

Установите библиотеку:
- `pip install git+https://github.com/syeysk/sy_api.git`

Для доступа к микросервисам необходим токен, получить который можно на странице "Токены для API":
<p align="center"><img src="getting_token_item.png" align="middle" width="65%"></p>

Для каждого микросервиса - отдельный токен.

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

## План разработки библиотеки

- [Дорожная карта](ROADMAP.md)