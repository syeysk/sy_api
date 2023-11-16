# Сущность "Ресурс"

Пример:
```python
from syapi import Resource

token = 'here-your-token'
resource = Resource(token)

resource_data = resource.create(title='My test resource', status=Resource.STATUS_REQUIRED)
print(resource.get(resource_data['id']))
```

Выведет:
```json
{"id": 1, "title": "My test resource", "status":  2}
```

## Описание методов

### Добавить новый ресурс

`Resource.create(title, status, fabric_maker=None)`:
- `title` - наименование ресурса
- `status` - статус ресурса. Значением является одна из констант `Resource.STATUS_*`
- `fabric_maker` - идентификатор фабрики-изготовителя ресурса, необязательный аргумент

Вернёт словарь вида `{"id": "integer"}`

### Получить описание ресурса

`Resource.get(resource_id)`:
- `resource_id` - идентификатор ресурса

Вернёт словарь вида `{"id": "integer", "title": "string", "status": "integer", "fabric_maker": "integer"}`

### Взять первый попавшийся ресурс на изготовление

`Resource.take_any_to_make(fabric_id)`:
- `fabric_id` - идентификатор фабрики, которая берёт ресурс

Вернёт словарь вида `{"id": "integer", "title": "string"}`, содержащий данные ресурса, который необходимо изготовить.
Если потребности в изготовлении какого-либо подходящего ресурса нет, то метод вернёт `None`. 
Ресурс будет отдан на изготовление, если статус ресурса равен `Resource.STATUS_REQUIRED`,
сразу после отдачи его статус будет изменён на `Resource.STATUS_IN_MAKING`.
