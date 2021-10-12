from cryptography.fernet import Fernet
from . import encryptor
import os


def get_decrypted_content(password, filepath=os.path.abspath('databases/database.db')) -> str:
    """
    Returns the unencrypted content of the database file
    :param password:
    :param filepath:
    :return: Decrypted content of the database file
    """
    with open(filepath, 'rb') as f:
        data = f.read()

    with open(filepath + ".salt", "rb") as f:
        salt = f.read()

    key, salt = encryptor.generate_key_using_password(password, salt)
    fernet = Fernet(key)
    unencrypted_data = fernet.decrypt(data)

    return unencrypted_data.decode()
