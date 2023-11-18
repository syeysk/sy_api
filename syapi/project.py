from syapi.base import BaseEntity
from syapi.constants import URL_MICROSERVICE_PLATFORM


class Project(BaseEntity):
    entity_code = 'project'
    DEFAULT_URL_MICROSERVICE = URL_MICROSERVICE_PLATFORM
