import requests

from syapi.exceptions import (
    AccessDeniedException,
    AlreadyExistsException,
    FieldsException,
    ObjectNotFoundException,
    ServerException,
)


class BaseEntity:
    DEFAULT_URL_MICROSERVICE = None
    entity_code = None

    def __init__(self, token: str, version: str | int = 1, url: str = None):
        if self.DEFAULT_URL_MICROSERVICE is None:
            raise Exception('You need to set "DEFAULT_URL_MICROSERVICE" constant.')

        if self.entity_code is None:
            raise Exception('You need to set "entity_code" property.')

        self.token = f'Bearer {token}'
        self.version = version
        self.url_microservice = url or self.DEFAULT_URL_MICROSERVICE

    @property
    def root_url(self):
        return f'{self.url_microservice}/api/v{self.version}/{self.entity_code}'

    def request(self, http_method, path, *args, **kwargs):
        headers = kwargs.setdefault('headers', {})
        headers.setdefault('Authorization', self.token)
        response = getattr(requests, http_method)(f'{self.root_url}{path}', *args, **kwargs)
        if response.status_code == 400:
            raise FieldsException(response.json())

        if response.status_code == 500:
            raise ServerException(response.content)

        if response.status_code == 403:
            raise AccessDeniedException(response.json()['detail'])

        if response.status_code == 404:
            raise ObjectNotFoundException(response.content)

        if response.status_code == 422:
            raise AlreadyExistsException(response.json()['detail'])

        return response
