from loguru import logger
from modules.login import *
from modules.connection import *
from modules.create_folders import *

# Initialize
create_base_folders()
logger.add('/logs/error.log')

user = User()
connection = ServerConnection()


# Functions
def registration():
    username = str(input('Choose username: '))
    while True:
        if connection.check_username(username):
            break
        username = str(input('This username is busy. Choose another'))
    while True:
        password1 = input('Enter password: ')
        password2 = input('Repeat password: ')
        if password1 == password2:
            break
        print('Passwords doesnt match. Try again!')
    response = connection.sign_up(username, password1)
    if response and response is bool:
        print('Successful registration')
        user.new_login(username, password1)


# Chat loop
while True:
    if user.is_logged():
        command = input('~$ ')
    else:
        login = str(input('Enter username: '))
        password = str(input('Enter password: '))
        call_back = connection.login(login, password)
        if call_back == 'logged':
            user.new_login(login, password)
        elif call_back == 'password_error':
            print("Password isn't correct")
            continue
        elif call_back == 'no user':
            print('No user found with this nickname')
            next_action = int(input('Select menu item: \n    1 - Registration section\n   2 = Exit app'))
            if next_action - 1:
                registration()
            else:
                break
        else:
            print(call_back)
