# Imports
import os
from getpass4 import getpass
from modules import server, user

# Initialize root dir path
base_dir = os.path.abspath(os.path.dirname(__file__))

# Initialize classes
connection = server.ServerConnection(base_dir)
user_obj = user.User(base_dir)


# Functuons
def not_logged():
    command = int(input("""Until you are logged into your account. Select menu item\n    1 - Login\n    2 - Registration\n~ """))
    if command-1:
        registration()
    else:
        login()

def login():
    username = str(input('Enter username: '))
    password = str(getpass('Enter password: '))
    responce = connection.login(username, password)
    if responce:
        print(responce)
        user_obj.login(username, password)
        return
    print('An error occured. Try again later')
    login()

def registration():
    username = str(input('Enter username: ')) 
    password1 = str(getpass('Enter password: '))
    password2 = str(getpass('Repeat password: '))
    if password1 == password2:
        responce = connection.registration(username, password)
        if responce:
            user_obj.login(username, password1)
            return
        print('An error occured. Try again latet')
        return
    print('Password doest match try again!')
    registration()

if not os.path.exists(f'{base_dir}/cdata/session.session') or len(open(f'{base_dir}/cdata/session.session').read()) < 1:
    user_obj.create_session()

# Main loop
while True:
    if user_obj.is_logged()['logged']:
        pass
    else:
        not_logged() 
