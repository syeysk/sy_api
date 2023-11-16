# Сущность "Фабрика"

Пример:
```python
from syapi import Fabric

token = 'here-your-token'
fabric = Fabric(token)

fabric_data = fabric.create(title='My test fabric')
print(fabric.get(fabric_data['id']))
```

Выведет:
```json
{"id": 1, "title": "My test fabric"}
```

## Описание методов

### Добавить новую фабрику

`Fabric.create(title)`:
- `title` - наименование фабрики

Вернёт словарь вида `{"id": "integer"}`

### Получить описание фабрики

`Fabric.get(fabric_id)`:
- `fabric_id` - идентификатор фабрики

Вернёт словарь вида `{"id": "integer", "title": "string"}`
