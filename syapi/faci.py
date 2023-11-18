from syapi.base import BaseEntity
from syapi.constants import URL_MICROSERVICE_FACI


class Faci(BaseEntity):
    entity_code = 'faci'
    DEFAULT_URL_MICROSERVICE = URL_MICROSERVICE_FACI
