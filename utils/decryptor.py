from cryptography.fernet import Fernet
from . import encryptor
import os


def get_decrypted_content(password, filepath=os.path.abspath('databases/database.db')) -> str:
    with open(filepath, 'rb') as f:
        data = f.read()

    key = encryptor.generate_key_using_password(password)
    fernet = Fernet(key)
    unencrypted_data = fernet.decrypt(data)

    return unencrypted_data.decode()
