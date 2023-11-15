from urllib.parse import quote

from syapi.base import BaseEntity
from syapi.constants import URL_MICROSERVICE_NOTE
from syapi.exceptions import (
    UnknownException,
)


class Note(BaseEntity):
    DEFAULT_URL_MICROSERVICE = URL_MICROSERVICE_NOTE
    entity_code = 'note'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.default_source = None

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
