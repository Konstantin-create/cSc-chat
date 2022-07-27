# Imports
import os
import sys
from getpass4 import getpass
from modules import server, user

# Initialize root dir path
base_dir = os.path.abspath(os.path.dirname(__file__))

# Initialize classes
connection = server.ServerConnection(base_dir)
user_obj = user.User(base_dir)


# Functuons
def clear_screen():
    if sys.platform == "linux" or sys.platform == "linux2":
        os.system('clear')
    elif sys.platform == "win32":
        os.system('cls')


def not_logged():
    command = int(
        input("""Until you are logged into your account. Select menu item\n    1 - Login\n    2 - Registration\n~ """))
    if command - 1:
        clear_screen()
        registration()
    else:
        clear_screen()
        login()


def logged():
    user = user_obj.is_logged()
    if connection.check_session(user['user']['id'], user['user']['username'], user['user']['password_hash'])['logged']: 
        print(f"Logged as {user['user']['username']}")
        print()
        print()
        responce = connection.get_user_chats(user['user']['id'])
        if not responce['success']:
            print('A server error occured. Try 2 minutes later')
            sys.exit()
        if responce['chats']:
            if len(responce['chats']) > 1:
                print('User chats: ')
            else:
                print('User chat: ')
            for i in range(len(responce['chats'])):
                print(f"{i} - {responce['chats'][i]['chat_name']}")
            user_obj.set_chats(responce['chats'])
            print()
            print(f"d - delete chat")
            print(f"e - exit")
            command = input('~ ')
            if command is int:
                pass  # Вывод сообщений чата
            else:
                if command.lower().strip() == 'd':
                    clear_screen()
                    delete_chat_menu()
                if command.lower().strip() == 'e':
                    sys.exit()
        else:
            user_obj.set_chats([])
            print('This user have no chats')
            if int(input('Select menu item:\n    1 - Create new chat\n    2 - Join chat by chat id\n~ ')) - 1:
                pass  # Function to join chat
            else:
                create_chat()
    else:
        user_obj.logout()
        not_logged()
        


def login():
    username = str(input('Enter username: '))
    password = str(getpass('Enter password: '))
    responce = connection.login(username, password)
    if responce:
        if responce['success'] and responce['logged']:
            responce_id = connection.get_id_by_username(username, password)
            if responce_id and responce_id['success']:
                user_obj.login(responce_id['user_id'], username, password)
                print('Restart program')
                sys.exit()
            else:
                clear_screen()
                print('An error occured. Try again later')
        else:
            clear_screen()
            print('Username or password are incorrect')
    else:
        clear_screen()
        print('An error occured. Try again later')
    login()


def registration():
    username = str(input('Enter username: '))
    password1 = str(getpass('Enter password: '))
    password2 = str(getpass('Repeat password: '))
    if password1 == password2:
        clear_screen()
        if not (int(input(
                f'Is everything right?\n    Username:{username}\n    Password:{password1}\n1 - Yes\n2- No\n~ ')) - 1):
            responce = connection.registration(username, password1)
            if responce:
                responce_id = connection.get_id_by_username(username, password1)
                if responce_id and responce_id['success']:
                    if responce['success'] and responce['is_registered']:
                        user_obj.login(responce_id['user_id'], username, password1)
                        return
                    else:
                        clear_screen()
                        print('User is already exists!')
                else:
                    clear_screen()
                    print('An error occured. Try again latet')
            else:
                clear_screen()
                print('An error occured. Try again later')
        else:
            clear_screen()
            if int(input('1 - Fil out registration form again\n2 - Back\n~ ')) - 1:
                clear_screen()
                not_logged()
    else:
        clear_screen()
        print('Password doest match try again!')
    registration()


def create_chat():
    chat_name = input('Enter chat name: ').strip()
    user = user_obj.is_logged()['user']
    if connection.get_chat_info_by_name(chat_name)['chat']:
        clear_screen()
        print('This chat name is already taken. Try anouther')
        create_chat()
    else:
        responce = connection.create_chat(chat_name, user['id'], user['password_hash'])
        if responce['success']:
            if responce['chat']:
                print('Chat has been created')
                print(responce['chat'])
                user_obj.add_chat_to_chats(responce['chat'])
                return
        print('An server error occured. Try again later')

def delete_chat_menu():
    user = user_obj.is_logged()
    responce = connection.get_user_chats(user['user']['id'])
    for i in range(len(responce['chats'])):
        print(f'{i} - {responce["chats"][i]["chat_name"]}')
    command = input('\nEnter chat number from list(b - to go back): ')
    if command.isdigit() and int(command) <= len(responce["chats"])+1:
        print(responce['chats'][int(command)])
        connection.delete_chat_by_name(responce['chats'][int(command)]['chat_name'], user['user']['id'], user['user']['password_hash'])
        sys.exit()
    elif command.lower().strip() == 'b':
        clear_screen()
        logged()
    else:
        clear_screen()
        print('Enter number!')
        print()
        delete_chat_menu()


if not os.path.exists(f'{base_dir}/cdata/session.session') or len(open(f'{base_dir}/cdata/session.session').read()) < 1:
    user_obj.create_session()

# Main loop
while True:
    clear_screen()
    if user_obj.is_logged()['logged']:
        logged()
        break
    else:
        not_logged()
