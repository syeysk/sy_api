from syapi.base import BaseEntity
from syapi.constants import URL_MICROSERVICE_RESOURCE
from syapi.exceptions import (
    UnknownException
)


class Fabric(BaseEntity):
    DEFAULT_URL_MICROSERVICE = URL_MICROSERVICE_RESOURCE
    entity_code = 'fabric'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def create(self, title: str):
        """
        Create a fabric.
        :param title: title of a fabric
        :return: {"id": "integer"} or raise an exception
        """
        response = self.request('post', '/new', json={'title': title})
        if response.status_code == 201:
            return response.json()

        raise UnknownException(response.status_code)

    def get(self, fabric_id: int | str):
        """
        Get a fabric.
        :param fabric_id: a fabric's id
        :return: {"id": "integer", "title": "string"} or raise an exception
        """
        response = self.request('get', f'/{fabric_id}', json={})
        if response.status_code == 200:
            return response.json()

        raise UnknownException(response.status_code)
