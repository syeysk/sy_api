import base64

from cryptography.hazmat.primitives import serialization as crypto_serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.backends import default_backend as crypto_default_backend


def generate_keys():
    key = rsa.generate_private_key(
        backend=crypto_default_backend(),
        public_exponent=65537,
        key_size=2048
    )
    return key, key.public_key()


def load_private_key(private_key: bytes):
    return crypto_serialization.load_pem_private_key(private_key, password=None)


def load_public_key(public_key: bytes):
    return crypto_serialization.load_pem_public_key(public_key, backend=crypto_default_backend())


def dumps_public_key(public_key):
    return public_key.public_bytes(
        encoding=crypto_serialization.Encoding.PEM,
        format=crypto_serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode()


def dumps_private_key(private_key):
    return private_key.private_bytes(
        encoding=crypto_serialization.Encoding.PEM,
        format=crypto_serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=crypto_serialization.NoEncryption()
    ).decode()


def encrypt(data: bytes, public_key) -> str:
    portions = []
    portion_size = 190
    portion = data[:portion_size]
    while portion:
        encrypted_portion = public_key.encrypt(
            portion,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        portions.append(encrypted_portion)
        portion = data[len(portions) * portion_size:portion_size * (len(portions) + 1)]

    return base64.b64encode(b''.join(portions)).decode()


def decrypt(encoded_base64: str, private_key) -> str:
    encoded_bytes = base64.b64decode(encoded_base64)
    portions = []
    portion_size = 256

    portion = encoded_bytes[:portion_size]
    while portion:
        decrypted_portion = private_key.decrypt(
            portion,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        portions.append(decrypted_portion)
        portion = encoded_bytes[portion_size * len(portions):portion_size * (len(portions) + 1)]

    return b''.join(portions).decode()
