import base64

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet
import os


def generate_key_using_password(password, salt=os.urandom(16)) -> (bytes, bytes):
    """
    This function generates a key to the corresponding password
    :param salt:
    :param password:
    :return: A generated key using a password
    """
    byte_password = password.encode()
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(byte_password)), salt


def encrypt_file(key, filepath) -> None:
    """
    This function encrypts a file with the corresponding key
    :param key:
    :param filepath:
    :return:
    """
    with open(filepath, 'rb') as f:
        data = f.read()

    fernet = Fernet(key)
    encrypted_file = fernet.encrypt(data)

    with open(filepath, 'wb') as f:
        f.write(encrypted_file)
