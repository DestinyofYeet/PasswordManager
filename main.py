from consolemenu.items import FunctionItem, SubmenuItem
from consolemenu import ConsoleMenu
import json
import string
import random
import os
import pathlib
import sys

from utils import db_manager
from utils import utils

database = None


"""
######################################### Database functions #########################################
"""


def register_database(database_path):
    # stores the saved paths in %appdata%\.pwmanager\registers.json

    path = str(pathlib.Path(__file__).parent.absolute()) + "/data"
    # if it doesn't exist, create it
    if not os.path.exists(path):
        os.mkdir(path)
        with open(f"{path}/register.json", "w+") as f:
            json.dump({1: database_path}, f, indent=2)
        return
    # if register.json doesn't exist, create it
    if not os.path.exists(f"{path}/register.json"):
        with open(f"{path}/.pwmanager/register.json", "w+") as f:
            json.dump({1: database_path}, f, indent=2)
        return

    with open(f"{path}/register.json") as f:
        file = json.load(f)

    # checks for double entries
    for i in file.values():
        if i == database_path:
            return

    file[len(file.keys()) + 1] = database_path

    with open(f"{path}/register.json", "w") as f:
        json.dump(file, f, indent=2)


def database_enable():
    """
    This will 'select' a database for use
    """
    global database
    path = str(pathlib.Path(__file__).parent.absolute()) + "/data/register.json"
    if not os.path.exists(path):
        print("You need to create a database first!")
        input("\nEnter to continue")
        return

    with open(path) as f:
        file = json.load(f)
    while True:
        print("You will now see the different locations of database files, please select one and input it below! This "
              "will be used to store and show passwords! To go back to the menu without selecting anything, input "
              "'quit'!")
        print()
        for i in file.values():
            print(f"- {i}")
        print()
        select_database = input("Path: ")
        if select_database in ['q', 'quit']:
            return
        if not os.path.exists(select_database + "/database.db"):
            print("The path specified doesn't have a database!")
            input("Enter to continue")
            os.system("cls")
            continue
        else:
            if select_database not in file.values():
                register_database(select_database)
            database_path = select_database + "/database.db"
            database = db_manager.Database(database_path)
            print("Database selected!")
            break
    input("\nEnter to continue")


def database_setup():
    """
    this will create a database
    """
    print("Input 'quit' to go back to the menu\n")
    database_path = input("Input the full path to the database folder: ")
    if utils.should_quit(database_path):
        return
    if not os.path.exists(database_path):
        confirm_creation = input("The folder specified doesn't exist! Should it be created? y/n: ")
        while True:
            if confirm_creation.lower() == ('y' or 'yes'):
                os.mkdir(database_path)
                print("Folder created!")
                break
            else:
                print("Creation aborted!")
                input("\nPress enter to continue")
                return

    register_database(database_path)
    utils.create_database(database_path + "/database.db")
    input("\nEnter to continue")


def check_selected_database():
    """
    This is responsible for checking if a database has been selected
    """
    global database
    if not isinstance(database, db_manager.Database):
        print("You have no database selected")
    else:
        print(f"Database is selected from path {database.get_path()}")

    input("\nEnter to continue")


"""
######################################### Non-wrapping password functions #########################################
"""


def password_generator() -> None:
    """
    Generates a password and printing it on the screen for the user to use
    :return:
    """
    length_of_password = 0

    while length_of_password == 0:
        print("After specifying some options your generated password will be given to you. Type in 'quit' to quit\n")
        try:
            length_of_password_input = input("Enter the length of your password: ")
            if utils.should_quit(length_of_password_input):
                return
            length_of_password = int(length_of_password_input)
        except ValueError:
            print("Invalid input! Try again.\n")
            continue

    lowercase_check = None

    while lowercase_check is None:
        lowercase_check = utils.confirm(input("Do you want lowercase characters? y/n: "))

    uppercase_check = None

    while uppercase_check is None:
        uppercase_check = utils.confirm(input("Do you want uppercase characters? y/n: "))

    digit_check = None

    while digit_check is None:
        digit_check = utils.confirm(input("Do you want digits? y/n: "))

    symbol_check = None

    while symbol_check is None:
        symbol_check = utils.confirm(input("Do you want symbols? y/n: "))

    if lowercase_check is False and uppercase_check is False and symbol_check is False and digit_check is False:
        print("Not selected anything. Returning to menu")
    else:
        password_string = ""

        possible_strings = []
        if lowercase_check:
            possible_strings.append(string.ascii_lowercase)

        if uppercase_check:
            possible_strings.append(string.ascii_uppercase)

        if digit_check:
            possible_strings.append(string.digits)

        if symbol_check:
            possible_strings.append(string.punctuation)

        for i in range(length_of_password):
            password_string += random.choice(random.choices(possible_strings)[0])

        print(f"Password generated: {password_string}")

    input("\nEnter to continue")


"""
######################################### Database wrapper functions #########################################
"""


def show_database_entries():
    """
    This is the wrapper function for the database.show_all_entries() function since database has to be set in order for
    this to work
    """
    global database
    if not isinstance(database, db_manager.Database):
        print("Database not initialized yet! Please select a database to read from from the database menu!")
        input("\nEnter to continue")
        return

    database.show_all_entries()


def create_database_entry():
    """
    This is the wrapper function for the database.add_password() function since database has to be set in order for
    this to work
    """
    global database
    if not isinstance(database, db_manager.Database):
        print("Database not initialized yet! Please select a database to read from from the database menu!")
        input("\nEnter to continue")
        return

    database.add_password()


def modify_database_entry():
    """
    This is the wrapper function for database.modify_entry() since database has to be set in order for this to work
    """
    global database
    if not isinstance(database, db_manager.Database):
        print("Database not initialized yet! Please select a database to read from from the database menu!")
        input("\nEnter to continue")
        return

    database.modify_entry()


def delete_database_entry():
    """
    Wrapper function for database.delete_entry() since database hast to be set
    :return:
    """
    global database
    if not isinstance(database, db_manager.Database):
        print("Database not initialized yet! Please select a database to read from from the database menu!")
        input("\nEnter to continue")
        return

    database.delete_entry()


"""
######################################### About #########################################
"""


def about():
    """
    Some about info
    """
    print("About: \n")
    print("Coded by DestinyofYeet")
    print("Github: https://github.com/DestinyofYeet/PasswordManager")
    input("\nEnter to continue")


"""
######################################### 'Main' Code #########################################
"""

if __name__ == '__main__':

    # Creates the main Menu
    menu = ConsoleMenu(f"Passwordmanager UI", "Select an option!")

    # Creates the submenu 'Passwordmanager menu'
    password_stuff = ConsoleMenu("Passwordmanager menu", "Select an option!")
    password_stuff_submenu = SubmenuItem("Passwordmanager menu", password_stuff, menu)

    # Creates the individual components of the submenu 'Passwordmanager menu'
    password_stuff.append_item(FunctionItem("Show all stored entries", show_database_entries))
    password_stuff.append_item(FunctionItem("Add database entry", create_database_entry))
    password_stuff.append_item(FunctionItem("Modify database entry", modify_database_entry))
    password_stuff.append_item(FunctionItem("Delete database entry", delete_database_entry))
    password_stuff.append_item(FunctionItem("Password generator", password_generator))

    # Creates the submenu 'Database menu'
    database_stuff = ConsoleMenu(f"Database menu", "Select an option!")
    database_stuff_submenu = SubmenuItem("Database Menu", database_stuff, menu)

    # Creates the individual components of the submenu 'Database menu'
    database_stuff.append_item(FunctionItem("Create a new database", database_setup))
    database_stuff.append_item(FunctionItem("Select a database to read from", database_enable))
    database_stuff.append_item(FunctionItem("Check selected database", check_selected_database))

    # Everything gets added to the main Menu
    menu.append_item(database_stuff_submenu)
    menu.append_item(password_stuff_submenu)
    menu.append_item(FunctionItem("About", about))
    menu.show(True)
