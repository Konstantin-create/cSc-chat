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

def logged():
    user = user_obj.is_logged()
    print(user)
    # responce = connection.get_user_chats()

def login():
    username = str(input('Enter username: '))
    password = str(getpass('Enter password: '))
    responce = connection.login(username, password)
    if responce:
        if responce['success'] and responce['logged']:
            responce_id = connection.get_id_by_username(username, password)
            if responce_id and responce_id['success']: 
                user_obj.login(responce_id['user_id'], username, password)
                return
            else:
                print('An error occured. Try again later')
        else:
            print('Username or password are incorrect')
    print('An error occured. Try again later')           
    login()

def registration():
    username = str(input('Enter username: ')) 
    password1 = str(getpass('Enter password: '))
    password2 = str(getpass('Repeat password: '))
    if password1 == password2:
        if not (int(input('Is everything right&\n    Username:{username}\n    Password:{password1}\n1 - Yes\n2- No')) - 1):
            responce = connection.registration(username, password1)
            if responce:
                responce_id = connection.get_id_by_username(username, password1)
                if responce_id and responce_id['success']:
                    if responce['success'] and responce['is_registered']:
                        user_obj.login(responce_id['user_id'], username, password1)
                        return
                    else:
                        print('User is already exists!')
                else:
                    print('An error occured. Try again latet')
            else:
                print('An error occured. Try again later')
        else:
            pass # Todo back menu
    else:
        print('Password doest match try again!')
        registration()

if not os.path.exists(f'{base_dir}/cdata/session.session') or len(open(f'{base_dir}/cdata/session.session').read()) < 1:
    user_obj.create_session()

# Main loop
while True:
    if user_obj.is_logged()['logged']:
        # logged()
        pass
    else:
        not_logged() 
