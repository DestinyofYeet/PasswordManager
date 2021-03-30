import os

from cryptography.fernet import Fernet
from stdiomask import getpass

from utils import encryptor


def enter():
    """
    Will wait till the user presses enter
    :return:
    """
    input("\nPress enter to continue")


def confirm(input_):
    """
    Just some small helper function to help with converting yes or no input into True and False
    :param input_:
    :return: bool
    """
    if input_.lower() in ['y', 'yes']:
        return True
    elif input_.lower() in ['n', 'no']:
        return False
    else:
        return None


def clear_screen() -> None:
    """
    Clears the screen. Will be expanded to also be usable on linux
    """
    os.system("cls")


def create_database(filepath=os.path.abspath('databases/database.db')) -> None:
    """
    Wrapper function for __generate_database__
    :param filepath:
    :return:
    """
    password = getpass("Please enter the password to create the database with: ")
    confirm_password = getpass("Please confirm your password: ")
    if password != confirm_password:
        print("Passwords aren't the same, aborting!")
        return
    success = __generate_database__(password, filepath)
    if success:
        print(f"Successfully created a database with the password specified")
    else:
        print("Failed to create database")


def __generate_database__(password, filepath) -> bool:
    """
    Will setup the database. Gets called from create_database
    :param password:
    :param filepath:
    :return: Success
    """

    # asking for file overwriting
    if os.path.exists(filepath):
        while True:
            check = input("The file specified already exists, do you want to overwrite the file? y/n: ")
            if check.lower() == 'y':
                break

            elif check.lower() == 'n':
                return False

    key, salt = encryptor.generate_key_using_password(password)

    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(b'{}')
    with open(filepath, 'wb+') as f:
        f.write(encrypted_data)

    with open(filepath + ".salt", "wb+") as f:
        f.write(salt)

    print(f"Created .db file in '{filepath}'")
    return True


def has_entries(entries) -> bool:
    """
    Will check if the specified database has any entries
    :param entries:
    :return: Will return if the database has entries
    """
    if len(entries) == 0:
        print("No entries yet! Go create some.")
        enter()
        return False
    else:
        return True


def should_quit(string_given) -> bool:
    """
    This function determines if the string_given should exit
    :param string_given:
    :return: Returns if the string is 'q' or 'quit'
    """
    return string_given in ['q', 'quit']

