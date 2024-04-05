# Библиотека для доступа к управлению сущностями Платформы через API

## Перед использованием

Установите библиотеку:
- `pip install git+https://github.com/syeysk/sy_api.git`

Для доступа к микросервисам необходим токен, получить который можно на странице "Токены для API":
<p align="center"><img src="getting_token_item.png" align="middle" width="65%"></p>

Для каждого микросервиса - отдельный токен.

## Использование

Краткий пример:
```python
from syapi import Fabric, Note, Resource, User

## access data

email = 'your_email'
user_password = 'your-password1234'
token_microservice_note = 'your-secret-token'
token_microservice_resource = 'your-secret-token'

## init entities

user = User()
userdata = user.login_by_email(email, user_password)  # you can have access only to one user in present time
note = Note(token_microservice_note)
fabric = Fabric(token_microservice_resource)
resource = Resource(token_microservice_resource)

# use entities

print(user.get())

title = 'Title of your note'  # the note's title is note's unique id
note.create(title, 'The interesting content here')
print(note.get(title))

fabric_data = fabric.create(title='Your fabric beautiful name')
print(fabric.get(fabric_data['id']))

resource_i_want = resource.create(title='Your useful resource', status=Resource.STATUS_REQUIRED)
print(resource.get(resource_i_want['id']))
resource_i_have = resource.create(title='Resource you have', status=Resource.STATUS_EXISTED, fabric_maker=fabric_data['id'])
print(resource.get(resource_i_have['id']))
resource_to_make = resource.take_any_to_make(fabric_data['id'])  # any fabric can take your desired resource to make it

print(resource_to_make['id'] == resource_i_want['id'])
```

## Подробное описание методов и полей сущностей

### Микросервис заметок

- [Заметка](/docs/note.md)

### Микросервис авторизации

- [Пользователь](/docs/user.md)

### Микросервис ресурсов

- [Фабрика](/docs/fabric.md)
- [Ресурс](/docs/resource.md)

## План разработки библиотеки

- [Дорожная карта](ROADMAP.md)