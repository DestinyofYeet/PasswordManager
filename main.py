from consolemenu.items import FunctionItem, SubmenuItem
from consolemenu import ConsoleMenu
import json
import traceback
from stdiomask import getpass

import os

from utils import db_manager

database = None


def register_database(database_path):
    path = os.getenv("appdata")
    if not os.path.exists(f"{path}\\.pwmanager\\"):
        os.mkdir(f"{path}\\.pwmanager\\")
        with open(f"{path}\\.pwmanager\\register.json", "w+") as f:
            json.dump({1: database_path}, f, indent=2)
        return

    if not os.path.exists(f"{path}\\.pwmanager\\register.json"):
        with open(f"{path}\\.pwmanager\\register.json", "w+") as f:
            json.dump({1: database_path}, f, indent=2)
        return

    with open(f"{path}\\.pwmanager\\register.json") as f:
        file = json.load(f)

    # checks for double entries
    for i in file.values():
        if i == database_path:
            return

    file[len(file.keys()) + 1] = database_path

    with open(f"{path}\\.pwmanager\\register.json", "w") as f:
        json.dump(file, f, indent=2)


def database_enable():
    global database
    path = os.getenv("appdata") + "\\.pwmanager\\register.json"
    if not os.path.exists(path):
        print("You need to create a database first!")
        input("\nEnter to continue")
        return

    with open(path) as f:
        file = json.load(f)
    while True:
        print("You will now see the different locations of database files, please select one and input it below! This will be used to store and show passwords! To go back to the menu without selecting anything, input 'quit'!")
        print()
        for i in file.values():
            print(f"- {i}")
        print()
        select_database = input("Path: ")
        if select_database in ['q', 'quit']:
            return
        if not os.path.exists(select_database + "\\database.db"):
            print("The path specified doesn't have a database!")
            input("Enter to continue")
            os.system("cls")
            continue
        else:
            if select_database not in file.values():
                register_database(select_database)
            database_path = select_database + "\\database.db"
            database = db_manager.Database(database_path)
            print("Database selected!")
            break
    input("\nEnter to continue")


def database_setup():
    print("Input 'quit' to go back to the menu\n")
    database_path = input("Input the full path to the database folder: ")
    if database_path in ['q', 'quit']:
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
    db_manager.create_database(database_path + "\\database.db")
    input("\nEnter to continue")


def check_selected_database():
    global database
    if not isinstance(database, db_manager.Database):
        print("You have no database selected")
    else:
        print(f"Database is selected from path {database.get_path()}")

    input("\nEnter to continue")


def show_database_entries():
    global database
    if not isinstance(database, db_manager.Database):
        print("Database not initialized yet! Please select a database to read from from the database menu!")
        input("\nEnter to continue")
        return

    database.show_all_entries()


def create_database_entry():
    global database
    if not isinstance(database, db_manager.Database):
        print("Database not initialized yet! Please select a database to read from from the database menu!")
        input("\nEnter to continue")
        return

    database.add_password()


def modify_database_entry():
    global database
    if not isinstance(database, db_manager.Database):
        print("Database not initialized yet! Please select a database to read from from the database menu!")
        input("\nEnter to continue")
        return

    database.modify_entry()


def about():
    print("About: \n")
    print("Coded by DestinyofYeet")
    print("Github: https://github.com/DestinyofYeet/PasswordManager")
    input("\nEnter to continue")


if __name__ == '__main__':

    menu = ConsoleMenu(f"Passwordmanager UI", "Select an option!")

    password_stuff = ConsoleMenu("Passwordmanager menu", "Select an option!")
    password_stuff_submenu = SubmenuItem("Passwordmanager menu", password_stuff, menu)

    password_stuff.append_item(FunctionItem("Show all stored entries", show_database_entries))
    password_stuff.append_item(FunctionItem("Add database entry", create_database_entry))
    password_stuff.append_item(FunctionItem("Modify database entry", modify_database_entry))

    database_stuff = ConsoleMenu(f"Database menu", "Select an option!")
    database_stuff_submenu = SubmenuItem("Database Menu", database_stuff, menu)

    database_stuff.append_item(FunctionItem("Create a new database", database_setup))
    database_stuff.append_item(FunctionItem("Select a database to read from", database_enable))
    database_stuff.append_item(FunctionItem("Check selected database", check_selected_database))

    menu.append_item(database_stuff_submenu)
    menu.append_item(password_stuff_submenu)
    menu.append_item(FunctionItem("About", about))
    menu.show(True)

