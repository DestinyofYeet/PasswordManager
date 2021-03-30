Password Manager
===========
## A simple password manager written in python

### How to use

A few things to be noted before you get started.
* The project is available on windows and linux, but i didn't confirm linux yet, although there should be nothing stopping it from running there.
* You don't need any specific python version. As long as the dependencies install you're fine.
* Note that with time the numbers for the different options could change. I'd suggest you watch out for the options name and not the number.

Download
---------

1. First clone the repository to your desired location
   

    $ git clone https://github.com/DestinyofYeet/PasswordManager.git

2. Then install the dependencies


    $ py -3.x -m pip intall -r requirements.txt

3. Starting the program is also very simple

    
    $ py -3.x main.py



Setup
-----

Before you can start putting in your passwords and information, you first have to create a database. The setup can all be done from inside the script

After starting the program, you are greeted with this screen.


```
  ┌─────────────────────────────────────────────────────────────────────────┐
  │                                                                         │
  │  Passwordmanager UI                                                     │
  │                                                                         │
  │  Select an option!                                                      │
  │                                                                         │
  │                                                                         │
  │    1 - Database menu                                                    │
  │    2 - Passwordmanager menu                                             │
  │    3 - About                                                            │
  │    4 - Exit                                                             │
  │                                                                         │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘
  >>
```

To create a database we are going to switch to the 'Database menu'

```
  ┌─────────────────────────────────────────────────────────────────────────┐
  │                                                                         │
  │  Database Menu                                                          │
  │                                                                         │
  │  Select an option!                                                      │
  │                                                                         │
  │                                                                         │
  │    1 - Create a new database                                            │
  │    2 - Select a database to read from                                   │
  │    3 - Check selected database                                          │
  │    4 - Return to Passwordmanager UI                                     │
  │                                                                         │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘
  >>
```
Once there, hit 1 for 'Create a new database'.

```
Input 'quit' to go back to the menu

Input the full path to the database folder:
```

As the program tells you, you can always exit out of any option by inputting 'quit' and hitting enter.

Here you can provide a new path to a folder where you want to have your database stored.

In this guide, I will have my path in `C:\Users\Admin\Database\` but you are free to put it else where. Just note that 
as of now, the script can only create a one-layer folder, for example it could create `C:\Users\Admin\Database` but not 
`C:\Users\Admin\Database\Database` since only the Admin, which is my user folder, exists.

````
Input 'quit' to go back to the menu

Input the full path to the database folder: C:\Users\Admin\Database
````

After hitting enter, it will ask you if you want to create the folder, if it doesn't exist.

```
Input 'quit' to go back to the menu

Input the full path to the database folder: C:\Users\Admin\Database
The folder specified doesn't exist! Should it be created? y/n: y
```

Say 'y' and hit enter.

Then you need to specify a password for your database. Note that this is the password which you need to view all of your
other passwords so choose one which is strong and which you can remember easily or write it on a piece of paper and secure it.

After creating a database you will get thrown back in the 'Database menu'.

Now you have successfully created a database with password.

Adding passwords
---------------

To access the database, you have to select the database first. To do that hit the 2 for 'Select a database to read from'.

Then you will see the path that you specified earlier. If you have created multiple databases they will also show up here. 
I've found it very convenient to have them show up here so you don't have to memorize the paths. 

For those who are curious the path's are stored in `%appdata%\.pwmanager\register.json`

```
You will now see the different locations of database files, please select one and input it below! This will be used to store and show passwords! To go back to the menu without selecting anything, input 'quit'!

- C:\Users\Admin\Database

Path: C:\Users\Admin\Database
```

Copy the path above into the input and hit enter.

You will then be prompted to input your password which you specified earlier.

```
You will now see the different locations of database files, please select one and input it below! This will be used to store and show passwords! To go back to the menu without selecting anything, input 'quit'!

- C:\Users\Admin\Database

Path: C:\Users\Admin\Database
Input your database password: ******************
```

After entering it correct you will have it selected

```
You will now see the different locations of database files, please select one and input it below! This will be used to store and show passwords! To go back to the menu without selecting anything, input 'quit'!

- C:\Users\Admin\Database

Path: C:\Users\Admin\Database
Input your database password: *******************
Checking password...Correct! Proceeding
Database selected!

Enter to continue
```
Hit enter to go back to the main menu.

You can **optionally** hit the 3 to see if you have a database selected.

```
Database is selected from path C:\Users\Admin\Database\database.db

Enter to continue
```

Once you got your database selected, hit the 4 to exit out of the 'Database menu' and get back to the main menu.

From the main menu hit the 2 for the 'Passwordmanager menu'.

Since you now have the database selected you can now create an entry!

```
  ┌─────────────────────────────────────────────────────────────────────────┐
  │                                                                         │
  │  Passwordmanager menu                                                   │
  │                                                                         │
  │  Select an option!                                                      │
  │                                                                         │
  │                                                                         │
  │    1 - Show all stored entries                                          │
  │    2 - Add database entry                                               │
  │    3 - Modify database entry                                            │
  │    4 - Return to Passwordmanager UI                                     │
  │                                                                         │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘
  >>
```
Hit the 2 to create an entry.

```
If you type in 'q' or 'quit' in the 'Website or usage' field, the program will abort the adding and go back to the menu

Website or usage:
```

Type in however you want to save it under. For example this could be `https://google.com` or `google main account`. 
Anything you can recognize it under.

Note that you don't have to fill out every field, for example you can leave the username or any other field blank but the 'Website or usage' field.

I will go for `https://example.com`.

```
If you type in 'q' or 'quit' in the 'Website or usage' field, the program will abort the adding and go back to the menu

Website or usage: https://example.com
Username:
```
You can now input a username.

```
If you type in 'q' or 'quit' in the 'Website or usage' field, the program will abort the adding and go back to the menu

Website or usage: https://example.com
Username: example
Description:
```

You can now provide a description of what you just put in. As said, you can leave it blank if you don't want to put in anything.

```
If you type in 'q' or 'quit' in the 'Website or usage' field, the program will abort the adding and go back to the menu

Website or usage: https://example.com
Username: example
Description: This is an example text
Password (will be hidden):
```
You can now put in a password for said site.

```
If you type in 'q' or 'quit' in the 'Website or usage' field, the program will abort the adding and go back to the menu

Website or usage: https://example.com
Username: example
Description: This is an example text
Password (will be hidden): ***************
Confirm password: ***************
Added password!

Enter to continue
```

After confirming said password, it will be added to your database. Press enter to get back to the menu.

Viewing passwords
----------------

To view a password, you have to be in the 'Passwordmaanger menu'. Then hit the 1 'Show all stored entries'.
```
  ┌─────────────────────────────────────────────────────────────────────────┐
  │                                                                         │
  │  Passwordmanager menu                                                   │
  │                                                                         │
  │  Select an option!                                                      │
  │                                                                         │
  │                                                                         │
  │    1 - Show all stored entries                                          │
  │    2 - Add database entry                                               │
  │    3 - Modify database entry                                            │
  │    4 - Return to Passwordmanager UI                                     │
  │                                                                         │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘
  >> 1
```

Now you will see whatever you put in the 'Website or usage' field.

I will see my `https://example.com` since I put that in my field.

```
You will now be listed all entries of your database. To get more information on one write the title of it in the console and press enter. Type in 'quit' to get back to the menu

- https://example.com

More information on:
```

Now to see the other information you put in earlier, just copy whatever you want to see in the 'More information on: ' field.

```
You will now be listed all entries of your database. To get more information on one write the title of it in the console and press enter. Type in 'quit' to get back to the menu

- https://example.com

More information on: https://example.com
```

Then hit enter.

```
You will now be listed all entries of your database. To get more information on one write the title of it in the console and press enter. Type in 'quit' to get back to the menu

- https://example.com

More information on: https://example.com
Username: example
Description: This is an example text

Show password? y/n:
```
There you can see the username and description you specified earlier.

To see the password you have to explicitly say that you want to see it by saying 'y' and pressing enter.

```
You will now be listed all entries of your database. To get more information on one write the title of it in the console and press enter. Type in 'quit' to get back to the menu

- https://example.com

More information on: https://example.com
Username: example
Description: This is an example text

Show password? y/n: y

Password: examplepassword

Press enter to continue
```

If you now press enter, you will not get back to the menu. You will get thrown back into the option to view more data.
To get back to the menu, you have to input 'quit' in the 'More information on: ' field.

```
You will now be listed all entries of your database. To get more information on one write the title of it in the console and press enter. Type in 'quit' to get back to the menu

- https://example.com

More information on: q
```
And press enter.

Modifying entries
-----------------
In addition to adding and viewing entries you also have the option of modifying them.

To do that you have to once again be in the 'Passwordmanager menu' and hit the 3 for 'Modify datbase entry'.

```
  ┌─────────────────────────────────────────────────────────────────────────┐
  │                                                                         │
  │  Passwordmanager menu                                                   │
  │                                                                         │
  │  Select an option!                                                      │
  │                                                                         │
  │                                                                         │
  │    1 - Show all stored entries                                          │
  │    2 - Add database entry                                               │
  │    3 - Modify database entry                                            │
  │    4 - Return to Passwordmanager UI                                     │
  │                                                                         │
  │                                                                         │
  └─────────────────────────────────────────────────────────────────────────┘
  >> 3
```
And hit enter.

You will get a similar screen as in viewing the data, but this one serves a different purpose.

Now lets say I want to change my 'This is an example text' description to 'This example is much cooler'.

Then I would select my `https://example.org` out of the list.

```
You will now be listed all entries of your database. Select one and copy it below to modify it. Type in 'quit' to get back to the menu

- https://example.com

Entry to modify: https://example.com
```
Then I hit enter.

It's just like the progam says, if you want to change something, write it in the corresponding field. If not just hit enter on the field and leave it blank.
```
You will now be listed all entries of your database. Select one and copy it below to modify it. Type in 'quit' to get back to the menu

- https://example.com

Entry to modify: https://example.com

If you want to change something, write it. If not just press enter

Old entry:

Title: https://example.com
Username: example
Description: This is an example text
Password: *******

New Entry:

New title:
```
Now as you see I want to update the description, so I hit enter for 'New title' and for 'New username', but change my 'New description'.

```
You will now be listed all entries of your database. Select one and copy it below to modify it. Type in 'quit' to get back to the menu

- https://example.com

Entry to modify: https://example.com

If you want to change something, write it. If not just press enter

Old entry:

Title: https://example.com
Username: example
Description: This is an example text
Password: *******

New Entry:

New title:
New username:
New description: This is a much cooler example
New password:
Are you sure to update the description? y/n: y
Updated description


Updated entry: https://example.com


Enter to continue
```
I confirm that I want to update the description and so it does.

Now if we hit enter, hit 'q' to go back and hit 1 for 'Show all stored entries' and check our description there, you 
can see that it got updated. 

```
You will now be listed all entries of your database. To get more information on one write the title of it in the console and press enter. Type in 'quit' to get back to the menu

- https://example.com

More information on: https://example.com
Username: example
Description: This is a much cooler example

Show password? y/n: n

Password will remain hidden

Press enter to continue
```

##Issues & Pull requests
Feel free to open up an issue if you have any problems. Also feel free to submit pull requests.