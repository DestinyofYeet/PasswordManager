#!/home/ole/anaconda3/envs/PasswordManager/bin/python3
import json
import os
import pathlib
import random
import string

from YeetsMenu.Menu import Menu
from YeetsMenu.utils.option import Option

from utils import db_manager
from utils import utils

database = None

"""
######################################### Database functions #########################################
"""


def register_database(database_path):
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


def add_database():
    """
    This will add a database to select it
    """
    utils.clear_screen()
    _input = input("Path to database directory: ")

    if not os.path.exists(_input):
        print("That path doesn't have a database")
        return

    print("Directory exists...adding")

    register_database(_input)


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

    db_menu = Menu(
        "You will now see the different locations of database files, please select one and input it below! This "
        "will be used to store and show passwords!")

    def real_database_enable(db_path: str):
        global database
        full_db_path = db_path + "/database.db"
        if not os.path.exists(full_db_path):
            print("The path specified doesn't have a database")
            return

        database = db_manager.Database(full_db_path)

    for i in file.values():
        db_menu.add_selectable(Option(f"- {i}", real_database_enable, i))

    db_menu.run()


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
    if not isinstance(database, db_manager.Database) or not database.is_init:
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

    database.show_all_entries(database.show_more_information_on)


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

    database.show_all_entries(database.modify_entry)


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

    database.show_all_entries(database.delete_entry)


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
    menu = Menu("Passwordmanager UI")

    # Creates the submenu 'Passwordmanager menu'
    password_stuff = Menu("Passwordmanager menu")

    # Creates the individual components of the submenu 'Passwordmanager menu'
    password_stuff.add_selectable(Option("Show all stored entries", show_database_entries))
    password_stuff.add_selectable(Option("Add database entry", create_database_entry))
    password_stuff.add_selectable(Option("Modify database entry", modify_database_entry))
    password_stuff.add_selectable(Option("Delete database entry", delete_database_entry))
    password_stuff.add_selectable(Option("Password generator", password_generator))

    # Creates the submenu 'Database menu'
    database_stuff = Menu("Database menu")

    # Creates the individual components of the submenu 'Database menu'
    database_stuff.add_selectable(Option("Create a new database", database_setup))
    database_stuff.add_selectable(Option("Add a database", add_database))
    database_stuff.add_selectable(Option("Select a database to read from", database_enable))
    database_stuff.add_selectable(Option("Check selected database", check_selected_database))

    # Everything gets added to the main Menu
    menu.add_selectable(database_stuff)
    menu.add_selectable(password_stuff)
    menu.add_selectable(Option("About", about))
    menu.run()
