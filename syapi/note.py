from urllib.parse import quote

import requests

from syapi.constants import URL_MICROSERVICE_NOTE
from syapi.exceptions import (
    AlreadyExistsException,
    FieldsException,
    ObjectNotFoundException,
    ServerException,
    UnknownException,
)


class Note:
    def __init__(self, token: str, version: str | int = 1):
        self.token = f'Bearer {token}'
        self.version = version
        self.default_source = None
        self.url_microservice_note = URL_MICROSERVICE_NOTE

    @property
    def root_url(self):
        return f'{self.url_microservice_note}/api/v{self.version}/note'

    def request(self, http_method, path, *args, **kwargs):
        headers = kwargs.setdefault('headers', {})
        headers.setdefault('Authorization', self.token)
        response = getattr(requests, http_method)(f'{self.root_url}{path}', *args, **kwargs)
        if response.status_code == 400:
            raise FieldsException(response.json())

        if response.status_code == 500:
            raise ServerException(response.content)

        if response.status_code == 404:
            raise ObjectNotFoundException(response.json()['detail'])

        if response.status_code == 422:
            raise AlreadyExistsException(response.json()['detail'])

        return response

    def get(self, title: str, source: str = None):
        """
        Getting the note
        :param title: title of a note
        :param source:unique name of knowledge's database
        :return: {"content": "string", "title": "string", "source": "string"} or raise the exception
        """
        source = source or self.default_source
        title = quote(title)
        response = self.request('get', f'/{title}/', json={}, params={'source': source})
        if response.status_code == 200:
            return response.json()

        raise UnknownException(response.status_code)

    def create(self, title: str, content: str, source: str = None):
        """
        Create a note.
        :param title: title of a note
        :param content: content of a note
        :param source: unique name of knowledge's database
        :return: {"source": "string"} or raise an exception
        """
        source = source or self.default_source
        title = quote(title)
        response = self.request('post', f'/{title}/', json={'content': content}, params={'source': source})
        if response.status_code == 204:
            return

        raise UnknownException(response.status_code)

    def update(self, title: str, new_title: str = None, new_content: str = None, source: str = None):
        """
        Update a note.
        :param title: title of a note
        :param new_title: new title of a note
        :param new_content: new content of a note
        :param source: unique name of knowledge's database
        :return: None or raise an exception
        """
        source = source or self.default_source
        title = quote(title)
        request_data = {}
        if new_title:
            request_data['new_title'] = new_title

        if new_content:
            request_data['new_content'] = new_content

        response = self.request('put', f'/{title}/', json=request_data, params={'source': source})
        if response.status_code == 204:
            return

        raise UnknownException(response.status_code)

    def delete(self, title: str, source: str = None):
        """
        Delete a note.
        :param title: title of a note
        :param source: unique name of knowledge's database
        :return: None or raise an exception
        """
        source = source or self.default_source
        title = quote(title)
        response = self.request('delete', f'/{title}/', json={}, params={'source': source})
        if response.status_code == 204:
            return

        raise UnknownException(response.status_code)
