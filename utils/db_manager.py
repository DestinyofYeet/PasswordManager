from . import encryptor
from . import decryptor
from . import utils
from cryptography.fernet import Fernet
from cryptography.fernet import InvalidToken
from stdiomask import getpass
import os
import sys
import json


class Database:
    def __init__(self, db_path=os.path.abspath('databases/database.db')):
        """
        Gets everything ready to store and read data.
        :param db_path:
        """
        self.db_path = db_path
        self.password = getpass(prompt="Input your database password: ")
        sys.stdout.write("Checking password...")
        sys.stdout.flush()
        if self.__check_password__():
            sys.stdout.write("Correct! Proceeding\n")
            sys.stdout.flush()
        else:
            sys.stdout.write("Password is incorrect! Exiting\n")
            sys.stdout.flush()
            input("Enter to continue")
            exit(1)

    def __check_password__(self) -> bool:
        """
        Checks if the password given is the correct one by attempting to decrypt it
        :return: Success of decryption
        """
        try:
            decryptor.get_decrypted_content(self.password, self.db_path)
            return True
        except InvalidToken:
            return False

    def __save_file__(self, content) -> None:
        """
        Gets the json file (byte or string), encrypts it and slaps it in the file
        :param content:
        :return:
        """
        if type(content) == str:
            content.encode()

        with open(self.db_path + ".salt", "rb") as f:
            salt = f.read()

        content_to_write = json.dumps(content, indent=2).encode()
        key, salt = encryptor.generate_key_using_password(self.password, salt)
        fernet = Fernet(key)
        real_content_to_write = fernet.encrypt(content_to_write)
        with open(self.db_path, "wb") as f:
            f.write(real_content_to_write)

    def add_password(self) -> None:
        """
        This will add a entry in the database
        :return:
        """
        print("If you type in 'q' or 'quit' in the 'Website or usage' field, the program will abort the adding and go back to the menu\n")
        website_or_usage = input("Website or usage: ")
        if utils.should_quit(website_or_usage):
            return

        # assures a key so that it can't be emtpy
        while not website_or_usage:
            website_or_usage = input("Website or usage: ")
        username = input("Username: ")
        description = input("Description: ")
        while True:
            password = getpass("Password (will be hidden): ")
            password_confirm = getpass("Confirm password: ")

            if password != password_confirm:
                check = input("Passwords are not the same! Do you want to re-enter both passwords? y/n: ")
                if check.lower().strip() in ['y', 'yes']:
                    continue

                elif check.lower().strip() in ['n', 'no']:
                    print("Aborted adding key!")
                    return
            else:
                break

        db_content = decryptor.get_decrypted_content(self.password, self.db_path)
        passwords = json.loads(db_content)

        # checking if the key is already there
        try:
            _ = passwords[website_or_usage]
            while True:
                check = input(f"There is already an entry titled '{website_or_usage}', are you sure you want to overwrite it? y/n: ")
                if check.lower() in ['n', 'no']:
                    print("Aborting")
                    return
                if check.lower() in ['y', 'yes']:
                    print("Overwriting!")
                    break
        except KeyError:
            pass

        passwords[website_or_usage] = {
            "description": description,
            "username": username,
            "password": password
        }
        self.__save_file__(passwords)
        print("Added password!")
        input("\nEnter to continue")

    def real_show_all_entries(self) -> None:
        """
        Prints all entries to the screen
        :return:
        """
        entries = json.loads(decryptor.get_decrypted_content(self.password, self.db_path))
        if len(entries.keys()) == 0:
            print("No entries yet! Go create some.")
            input("Enter to continue")
            return
        print()
        for i in sorted(entries.keys()):
            print(f"- {i}")
        print()

    def show_all_entries(self) -> None:
        """
        Can more specifics about a dataset, like username, description and password
        :return:
        """
        # loads the entries and checks if there are any
        entries = json.loads(decryptor.get_decrypted_content(self.password, self.db_path))
        if len(entries.keys()) == 0:
            print("No entries yet! Go create some.")
            input("\nEnter to continue")
            return
        # infinite loop for looking up multiple things
        while True:
            print("You will now be listed all entries of your database. To get more information on one write the title of it in the console and press enter. Type in 'quit' to get back to the menu")
            self.real_show_all_entries()
            more_information_on = input("More information on: ").strip()
            if more_information_on:
                if utils.should_quit(more_information_on):
                    break
                else:
                    try:
                        more_info_entry = entries[more_information_on]
                        print(f"Username: {more_info_entry['username']}")
                        print(f"Description: {more_info_entry['description']}")
                        print()
                        show_password = input("Show password? y/n: ")
                        print()
                        if show_password.lower() == 'y':
                            print(f"Password: {more_info_entry['password']}")
                        else:
                            print(f"Password will remain hidden")
                        print()
                        input("Press enter to continue")

                    except KeyError:
                        print("You don't have an entry with that title!")
                        input("\nPress enter to continue")

            utils.clear_screen()

    def get_path(self) -> str:
        """
        Returns the path to the current selected database file
        :return: Path to the current selected database file
        """
        return self.db_path

    def modify_entry(self) -> None:
        """
        Allows a modification of an entry
        :return:
        """
        entries = json.loads(decryptor.get_decrypted_content(self.password, self.db_path))
        if len(entries.keys()) == 0:
            print("No entries yet! Go create some.")
            input("\nEnter to continue")
            return
        while True:
            print("You will now be listed all entries of your database. Select one and copy it below to modify it. Type in 'quit' to get back to the menu")
            self.real_show_all_entries()
            entry_to_modify = input("Entry to modify: ")
            if utils.should_quit(entry_to_modify):
                break
            if entry_to_modify:
                try:
                    entry_to_modify_entry = entries[entry_to_modify]
                    print("\nIf you want to change something, write it. If not just press enter\n")
                    print("Old entry:\n")
                    print(f"Title: {entry_to_modify}")
                    print(f"Username: {entry_to_modify_entry['username']}")
                    print(f"Description: {entry_to_modify_entry['description']}")
                    print(f"Password: {len(entry_to_modify_entry['password'])*'*'}")
                    print("\nNew Entry:\n")
                    new_title = input(f"New title: ")
                    new_username = input(f"New username: ")
                    new_description = input(f"New description: ")
                    new_password = getpass("New password: ")
                    confirm_new_password = ""
                    if new_password:
                        confirm_new_password = getpass("Confirm new password: ")

                    # checks till a) passwords are the same or b) user didn't want to change the passwords
                    while new_password != confirm_new_password:
                        check = input("The passwords don't match. Do you want to re-enter both? y/n: ")
                        check = utils.confirm(check)
                        if isinstance(check, bool):
                            if check is False:
                                new_password = ""
                                print("Ignoring new password")
                            else:
                                new_password = getpass("New password: ")
                                confirm_new_password = getpass("Confirm new password: ")

                    if new_password:
                        print("Passwords match")

                    title_gets_updated = False  # use of an extra variable to keep the modification in order: 1. Title 2. username etc...

                    if new_title:
                        check = None
                        while check is None:
                            check = input("Are you sure to update the title? y/n: ")
                            check = utils.confirm(check)
                        if check is True:
                            title_gets_updated = True
                            entries[new_title] = entries[entry_to_modify]
                            del entries[entry_to_modify]
                            print("Title got updated")
                        else:
                            print("Did not update title")
                        print()

                    if new_username:
                        check = None
                        while check is None:
                            check = input("Are you sure to update the username? y/n: ")
                            check = utils.confirm(check)
                        if check is True:
                            if not title_gets_updated:
                                entry_to_modify_entry['username'] = new_username
                            else:
                                entries[new_title]['username'] = new_username
                            print("Updated username")
                        else:
                            print("Did not update username")
                        print()

                    if new_description:
                        check = None
                        while check is None:
                            check = input("Are you sure to update the description? y/n: ")
                            check = utils.confirm(check)
                        if check is True:
                            if not title_gets_updated:
                                entry_to_modify_entry['description'] = new_description
                            else:
                                entries[new_title]['description'] = new_description
                            print("Updated description")
                        else:
                            print("Did not update description")
                        print()

                    if new_password:
                        check = None
                        while check is None:
                            check = input("Are you sure to update the password? y/n: ")
                            check = utils.confirm(check)
                        if check is True:
                            if not title_gets_updated:
                                entry_to_modify_entry['password'] = new_password
                            else:
                                entries[new_title]['password'] = new_password
                            print("Updated password")
                        else:
                            print("Did not update password")
                        print()

                    self.__save_file__(entries)
                    print(f"\nUpdated entry: {entry_to_modify}\n")

                except KeyError:
                    print("You don't have a entry titled like that!")

                input("\nEnter to continue")
                utils.clear_screen()

    def delete_entry(self) -> None:
        """
        This function has the ability to delete an entry
        :return:
        """
        entries = json.loads(decryptor.get_decrypted_content(self.password, self.db_path))
        while True:
            if not utils.has_entries(entries):
                return
            print("You will now be listed all entries of your database. Select one and copy it below to delete it. Type in 'quit' to get back to the menu")
            self.real_show_all_entries()
            print()

            entry_to_delete = input("Entry to delete: ")
            if not entry_to_delete:
                utils.clear_screen()
                continue

            if utils.should_quit(entry_to_delete):
                return

            try:
                entries[entry_to_delete]
            except KeyError:
                print("You don't have an entry named like that!")
                input("\nEnter to continue")
                utils.clear_screen()
                continue

            print("\nEntry:\n")
            print(f"Username: {entries[entry_to_delete]['username']}")
            print(f"Description: {entries[entry_to_delete]['description']}")
            print(f"Password: {len(entries[entry_to_delete]['password']) * '*'}\n")

            check = None
            while check is None:
                check = utils.confirm(input(f"Are you sure you want to delete the entry '{entry_to_delete}'? y/n: "))

            if check:
                del entries[entry_to_delete]
                self.__save_file__(entries)
                print("Entry has been deleted")
            else:
                print("Deletion has been aborted")

            input("\nEnter to continue")
            utils.clear_screen()
