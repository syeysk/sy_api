import json
from secrets import token_urlsafe
from random import randint

import requests
from syapi.constants import URL_MICROSERVICE_AUTH
from syapi.exceptions import (
    AccessDeniedException,
    AlreadyExistsException,
    FieldsException,
    ObjectNotFoundException,
    ServerException,
    UnknownException,
)
from syapi.utils import (
    decrypt,
    dumps_public_key,
    dumps_private_key,
    encrypt,
    generate_keys,
    load_public_key,
    load_private_key,
)


class User:
    def __init__(
        self,
        token: str = None,
        microservice_auth_id: str = None,
        auth_public_key: bytes = None,
        private_key: bytes = None,
        public_key: bytes = None,
        version: int | str = 1,
        url: str = None,
    ):
        self.token = token
        self.version = version
        self.microservice_auth_id = microservice_auth_id
        if None in (private_key, public_key):
            self._private_key, self._public_key = generate_keys()
        else:
            self._public_key = load_public_key(public_key)
            self._private_key = load_private_key(private_key)

        self.url_microservice_auth = url or URL_MICROSERVICE_AUTH
        if auth_public_key is None:
            self._auth_public_key = self._get_auth_public_key()
        else:
            self._auth_public_key = load_public_key(auth_public_key)

    @property
    def root_url(self):
        return f'{self.url_microservice_auth}/api/v{self.version}/auth'

    def _get_auth_public_key(self):
        response = requests.get(f'{self.root_url}/public_key/')
        return load_public_key(response.json()['public_key'].encode())

    def serialize(self):
        return {
            'token': self.token,
            'microservice_auth_id': self.microservice_auth_id,
            'auth_public_key': dumps_public_key(self._auth_public_key),
            'private_key': dumps_private_key(self._private_key),
            'public_key': dumps_public_key(self._public_key),
        }

    def request(self, http_method, path, use_token, *args, **kwargs):
        dict_data = kwargs.get('json', {})
        if use_token:
            dict_data['token'] = self.token
            dict_data['microservice_auth_id'] = self.microservice_auth_id

        dict_data['public_key'] = dumps_public_key(self._public_key)
        dict_data['random_trash'] = token_urlsafe(randint(5, 20))
        kwargs['json'] = {
            'data': encrypt(json.dumps(dict_data).encode(), self._auth_public_key),
        }
        response = getattr(requests, http_method)(f'{self.root_url}{path}', *args, **kwargs)
        if response.status_code == 400:
            raise FieldsException(self._decrypt(response))

        if response.status_code == 500:
            raise ServerException(response.content)

        if response.status_code == 403:
            raise AccessDeniedException(self._decrypt(response)['detail'])

        if response.status_code == 404:
            raise ObjectNotFoundException(self._decrypt(response)['detail'])

        if response.status_code == 422:
            raise AlreadyExistsException(self._decrypt(response)['detail'])

        return response

    def _decrypt(self, response):
        decrypted_data = json.loads(decrypt(response.json()['data'], self._private_key))
        del decrypted_data['random_trash']
        self._auth_public_key = load_public_key(decrypted_data.pop('public_key').encode())
        return decrypted_data

    def login(self, username, password):
        response = self.request('post', '/login/', False, json={'username': username, 'password': password})
        if response.status_code == 200:
            decrypt_data = self._decrypt(response)
            self.token = decrypt_data.pop('token')
            self.microservice_auth_id = decrypt_data['microservice_auth_id']
            return decrypt_data

        raise UnknownException(response.status_code)

    def registrate(self, username, password, email, first_name='', last_name=''):
        fields = {
            'username': username,
            'password': password,
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
        }
        response = self.request('post', '/registrate/', True, json=fields)
        if response.status_code == 200:
            decrypt_data = self._decrypt(response)
            self.token = decrypt_data.pop('token')
            self.microservice_auth_id = decrypt_data['microservice_auth_id']
            return decrypt_data

        raise UnknownException(response.status_code)

    def login_or_registrate_by_extern(self, username, email, extern_id, old_token, first_name='', last_name=''):
        fields = {
            'username': username,
            'extern_id': extern_id,
            'email': email,
            'first_name': first_name,
            'last_name': last_name,
            'old_token': old_token,
        }
        response = self.request('post', '/login_or_registrate_by_extern/', True, json=fields)
        if response.status_code == 200:
            decrypt_data = self._decrypt(response)
            self.token = decrypt_data.pop('token')
            self.microservice_auth_id = decrypt_data['microservice_auth_id']
            return decrypt_data

        raise UnknownException(response.status_code)

    def get(self):
        response = self.request('get', '/user/', True, json={})
        if response.status_code == 200:
            return self._decrypt(response)

        raise UnknownException(response.status_code)

    def put(self, **fields):
        response = self.request('put', '/user/', True, json=fields)
        if response.status_code == 200:
            return self._decrypt(response)

        raise UnknownException(response.status_code)

    def delete(self, password):
        response = self.request('delete', '/user/', True, json={'password': password})
        if response.status_code == 200:
            return

        raise UnknownException(response.status_code)
