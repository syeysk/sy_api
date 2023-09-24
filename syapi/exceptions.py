class FieldsException(Exception):
    status_code = 400

    def __init__(self, errors):
        self.errors = errors


class ObjectNotFoundException(Exception):
    status_code = 404


class AlreadyExistsException(Exception):
    status_code = 404


class ServerException(Exception):
    status_code = 500


class UnknownException(Exception):
    def __init__(self, status_code):
        self.status_code = status_code

