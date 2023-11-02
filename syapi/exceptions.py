class FieldsException(Exception):
    status_code = 400

    def __init__(self, errors):
        self.errors = errors


class NotAuthorizedException(Exception):
    status_code = 401


class AccessDeniedException(Exception):
    status_code = 403


class ObjectNotFoundException(Exception):
    status_code = 404


class AlreadyExistsException(Exception):
    status_code = 404


class ServerException(Exception):
    status_code = 500


class UnknownException(Exception):
    def __init__(self, status_code):
        self.status_code = status_code

