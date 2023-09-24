# Библиотека для доступа к микросервисам Платформы через API

## Использование

Установите библиотеку:
- `pip install git+https://github.com/syeysk/sy_api.git`

Для доступа к микросервисам необходим токен, получить который можно на странице "Токены для API":
<p align="center"><img src="getting_token_item.png" align="middle"></p>

Пример кода:
```python
from syapi.note import Note

token = 'here-your-token'
note = Note(token)

title = 'Заметка для теста'
content = 'а это её содержимое))'
note.create(title, content)
new_title = 'Заметка для теста (обновлён заголовок)'
note.update(title, new_title=new_title)
note.update(new_title, new_content='ну вот и содержимое обновилось')
note.delete(new_title)
```

## План разработки библиотеки

- [Дорожная карта](ROADMAP.md)