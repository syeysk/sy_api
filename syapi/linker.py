from syapi.base import BaseEntity
from syapi.exceptions import (
    UnknownException
)


class Linker(BaseEntity):
    DEFAULT_URL_MICROSERVICE = None
    entity_code = 'linker'

    def __init__(self, linked_what: BaseEntity):
        self.DEFAULT_URL_MICROSERVICE = linked_what.DEFAULT_URL_MICROSERVICE
        super().__init__(linked_what.token.split()[1], linked_what.version, linked_what.url_microservice)
        self.linked_entity_code = linked_what.entity_code

    def create(self, title: str):
        """
        Create a link.
        :param title: title of a fabric
        :return: {} or raise an exception
        """

    def get(
        self,
        link_to_id: int | str,
        linked_to: type[BaseEntity],
        page: int = None,
        on_page: int = None,
        order_by: list[str] = None,
        fields: list[str] = None,
        extra_fields: list[str] = None,
    ):
        """
        Get a links.
        :param link_to:
        :return: {} or raise an exception
        """
        request_data = {'object': self.linked_entity_code}
        if page:
            request_data['page'] = page

        if on_page:
            request_data['on_page'] = on_page

        if order_by:
            request_data['order_by'] = order_by

        if fields:
            request_data['fields'] = fields

        if extra_fields:
            request_data['extra_fields'] = extra_fields

        response = self.request('post', f'/get/{linked_to.entity_code}/{link_to_id}/', json=request_data)
        if response.status_code == 200:
            return response.json()

        raise UnknownException(response.status_code)
