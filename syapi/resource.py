from syapi.base import BaseEntity
from syapi.constants import URL_MICROSERVICE_RESOURCE
from syapi.exceptions import (
    UnknownException
)


class Resource(BaseEntity):
    STATUS_OTHER = 1
    STATUS_REQUIRED = 2
    STATUS_EXISTED = 3
    STATUS_IN_MAKING = 4
    DEFAULT_URL_MICROSERVICE = URL_MICROSERVICE_RESOURCE
    entity_code = 'resource'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def create(self, title, status, fabric_maker=None):
        """
        Create a resource.
        :param title: title of a resource
        :param status: id of status
        :param fabric_maker: id of fabric-maker
        :return: {"id": "integer"} or raise an exception
        """
        response = self.request('post', '/new', json={'title': title, 'status': status, 'fabric_maker': fabric_maker})
        if response.status_code == 201:
            return response.json()

        raise UnknownException(response.status_code)

    def get(self, resource_id: int | str):
        """
        Get a resource.
        :param resource_id: a resource's id
        :return: {"id": "integer", "title": "string", "status": "integer", "fabric_maker": "integer"}
         or raise an exception
        """
        response = self.request('get', f'/{resource_id}', json={})
        if response.status_code == 200:
            return response.json()

        raise UnknownException(response.status_code)

    def take_any_to_make(self, fabric_id):
        """
        Return the first resource to make.
        :param fabric_id: a fabric's id
        :return: {"id": "integer", "title": "string"} or raise an exception
        """
        response = self.request('put', '/take_any_to_make', json={'fabric': fabric_id})
        if response.status_code == 200:
            return response.json()

        if response.status_code == 204:
            return

        raise UnknownException(response.status_code)
