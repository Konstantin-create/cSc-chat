# Imports
import os
from getpass4 import getpass
from modules import server, user

# Initialize root dir path
base_dir = os.path.abspath(os.path.dirname(__file__))

# Initialize classes
connection = server.ServerConnection(base_dir)
user = user.User(base_dir)


# Functuons
def not_logged():
    command = int(input("""Until you are logged into your account. Select menu item\n    1 - Login\n    2) Registration"""))
    if command-1:
        login()
    else:
        registration()

def login():
    username = str(input('Enter username: '))
    password = str(getpass('Enter password: '))
    server

def registration():
    pass


# Main loop
while True:
    if user.is_logged():
        pass
    else:
        pass
