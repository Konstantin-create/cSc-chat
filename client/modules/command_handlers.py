import os
import sys
from getpass4 import getpass

from config import base_dir
from modules import user, server

connection = server.ServerConnection(base_dir)
user_obj = user.User(base_dir)


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
        response = connection.get_user_chats(user['user']['id'])
        if not response['success']:
            print('A server error occurred. Try 2 minutes later')
            sys.exit()
        if response['chats']:
            if len(response['chats']) > 1:
                print('User chats: ')
            else:
                print('User chat: ')
            for i in range(len(response['chats'])):
                print(f"{i} - {response['chats'][i]['chat_name']}")
            user_obj.set_chats(response['chats'])
            print()
            print('j - join chat by id')
            print('s - show user subscibtions')
            print('m - moderate chat')
            print('e - exit')
            print('l - logout from device')
            print('d - delete user')
            command = input('~ ')
            if command.isdigit() and int(command) <= len(response['chats']):
                chat_messages_menu(response['chats'][int(command)]['id'])
            elif command.lower().strip() == 'm':
                clear_screen()
                delete_chat_menu()
            elif command.lower().strip() == 'e':
                sys.exit()
            elif command.lower().strip() == 'l':
                user_obj.logout()
            elif command.lower().strip() == 'j':
                while True:
                    chanel_to_sub = input('Enter chat id to join(b - back):')
                    if chanel_to_sub.isdigit():
                        print(connection.subscribe_chat(int(chanel_to_sub), user['user']['id'],
                                                        user['user']['password_hash']))
                        break
                    elif chanel_to_sub.lower().strip() == 'b':
                        clear_screen()
                        logged()
                        break
                    else:
                        clear_screen()
                        print('Enter chat id or "b" to back!')
                        print()
            elif command.lower().strip() == 's':
                user_subscriptions()
            elif command.lower().strip() == 'd':
                delete_user_menu()
            else:
                clear_screen()
                logged()
        else:
            user_obj.set_chats([])
            print('This user have no chats')
            command = input(
                'Select menu item:\n    1 - Create new chat\n    2 - Join chat by chat id\n\ns - show usersubscriptions\ne - exit\nl - logout from devise\nd - delete user\n~ ')
            if command.isdigit():
                if int(command) - 1:
                    subscribe_chat_menu()
                else:
                    clear_screen()
                    create_chat()
            elif command.lower().strip() == 's':
                user_subscriptions()
            elif command.lower().strip() == 'e':
                sys.exit()
            elif command.lower().strip() == 'l':
                user_obj.logout()
            elif command.lower().strip() == 'd':
                delete_user_menu()
    else:
        user_obj.logout()
        not_logged()


def login():
    username = str(input('Enter username: '))
    password = str(getpass('Enter password: '))
    response = connection.login(username, password)
    if response:
        if response['success'] and response['logged']:
            response_id = connection.get_id_by_username(username, password)
            if response_id and response_id['success']:
                user_obj.login(response_id['user_id'], username, password)
                print('Restart program')
                sys.exit()
            else:
                clear_screen()
                print('An error occurred. Try again later')
        else:
            clear_screen()
            print('Username or password are incorrect')
    else:
        clear_screen()
        print('An error occurred. Try again later')
    login()


def registration():
    username = str(input('Enter username: '))
    password1 = str(getpass('Enter password: '))
    password2 = str(getpass('Repeat password: '))
    if password1 == password2:
        clear_screen()
        if not (int(input(
                f'Is everything right?\n    Username:{username}\n    Password:{password1}\n1 - Yes\n2- No\n~ ')) - 1):
            response = connection.registration(username, password1)
            if response:
                response_id = connection.get_id_by_username(username, password1)
                if response_id and response_id['success']:
                    if response['success'] and response['is_registered']:
                        user_obj.login(response_id['user_id'], username, password1)
                        return
                    else:
                        clear_screen()
                        print('User is already exists!')
                else:
                    clear_screen()
                    print('An error occurred. Try again latet')
            else:
                clear_screen()
                print('An error occurred. Try again later')
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
        print('This chat name is already taken. Try another')
        create_chat()
    else:
        response = connection.create_chat(chat_name, user['id'], user['password_hash'])
        if response['success']:
            if response['chat']:
                print('Chat has been created')
                print(response['chat'])
                user_obj.add_chat_to_chats(response['chat'])
                return
        print('An server error occurred. Try again later')


def delete_chat_menu():
    user = user_obj.is_logged()
    response = connection.get_user_chats(user['user']['id'])
    for i in range(len(response['chats'])):
        print(f'{i} - {response["chats"][i]["chat_name"]}')
    command = input('\nEnter chat number from list to delete chat(b - to go back): ')
    if command.isdigit() and int(command) <= len(response["chats"]):
        print(response['chats'][int(command)])
        connection.delete_chat_by_name(response['chats'][int(command)]['chat_name'], user['user']['id'],
                                       user['user']['password_hash'])
        sys.exit()
    elif command.lower().strip() == 'b':
        clear_screen()
        logged()
    else:
        clear_screen()
        print('Enter number!')
        print()
        delete_chat_menu()

def subscribe_chat_menu():
    clear_screen()
    user = user_obj.is_logged()
    while True:
        chanel_to_sub = input('Enter chat id to join(b - back):')
        if chanel_to_sub.isdigit():
            print(connection.subscribe_chat(int(chanel_to_sub), user['user']['id'],
                                            user['user']['password_hash']))
            break
        elif chanel_to_sub.lower().strip() == 'b':
            clear_screen()
            logged()
            break
        else:
            clear_screen()
            print('Enter chat id or "b" to back!')
            print()

def unsubscribe_chats_menu():
    user = user_obj.is_logged()
    response = connection.get_user_subscriptions(user['user']['id'], user['user']['password_hash'])
    if not response['success']:
        print('A server error occurred! Try again later')
        print()
        command = input('b - back')
        if command.lower().strip() == 'b':
            user_subscriptions()
        else:
            unsubscribe_chats_menu()
    elif response['chats']:
        for i in range(len(response['chats'])):
            print(f'{i} - {response["chats"][i]["chat_name"]}')
        command = input('\nEnter chat number from list to unsubscribe chat(b - back)')
        if command.isdigit() and int(command) <= len(response['chats']):
            pass  # todo unsubscribe func
        elif command.lower().strip() == 'b':
            user_subscriptions()
        else:
            clear_screen()
            print('Enter number or b')
            print()
            unsubscribe_chats_menu()
    else:
        user_subscriptions()


def user_subscriptions():
    clear_screen()
    user = user_obj.is_logged()
    response = connection.get_user_subscriptions(user['user']['id'], user['user']['password_hash'])
    if not response['success']:
        print('A server error occurred! Try again later')
    elif response['chats']:
        print('User chats:\n')
        for i in range(len(response['chats'])):
            print(f'{i} - {response["chats"][i]["chat_name"]}')
        print()
        print('Enter chat number to print messages')
        print('m - manage chats')
    else:
        print('This user have no subscibtions!')
    print()
    print('b - back')
    command = input('~ ')
    if command.isdigit():
        if int(command) <= len(response['chats']):
            chat_messages_menu(response['chats'][int(command)]['id'])
    elif command.lower().strip() == 'b':
        clear_screen()
        logged()
    elif command.lower().strip() == 'm':
        clear_screen()
        unsubscribe_chats_menu()
    else:
        user_subscriptions()

def delete_user_menu():
    clear_screen()
    user = user_obj.is_logged()
    command = input('Are you sure you want to permanently delete user {user["user"]["username"]}?\n    1 - Yes\n    2 - No(back)\n~ ')
    if command.isdigit():
        if int(command) - 1:
            clear_screen()
            logged()
        else:
            clear_screen()
            connection.delete_user(user['user']['username'], user['user']['password_hash'])
            logged()
    else:
        delete_user_menu()

def chat_messages_menu(chat_id):
    clear_screen()
    user = user_obj.is_logged()['user']
    response = connection.get_chat_messages(chat_id)
    if response['success']:
        if response['messages']:
            chat_usernames = {}
            dated_messages = {}
            for message in response['messages']:
                if not (message['from_user'] in chat_usernames):
                    chat_usernames[message['from_user']] = connection.get_username_by_id(message['from_user'])['username']
                time_stamp = message['time_stamp'].split()
                message_time_stamp = f'{time_stamp[0]} {time_stamp[1]} {time_stamp[2]} {time_stamp[3]}'
                if not message_time_stamp in dated_messages:
                    dated_messages[message_time_stamp] = []
                dated_messages[message_time_stamp].append(message)
            for key in dated_messages:
                print(('-' * 50).center(len(key) + 200))
                print(key.center(len(key)+200))
                for message in dated_messages[key]:
                    if chat_usernames[message['from_user']] == user['username']:
                        print('    From me')
                    else:
                        print(f'    From {chat_usernames[message["from_user"]]}')
                    print('    ' + message['body'])
                    print()
                    print()
            print('b - back', 'u - update messages', 'm - create new message')
            command = input('~ ')
            if command == 'b':
                clear_screen()
                logged()
            elif command == 'u':
                chat_messages_menu(chat_id)
            elif command == 'm':
                create_message_menu(chat_id)
        else:
            print("This chat have no messages! So it's time to be the first to post!")
            print("m - new message")
            print("b - back")
            command = input('~ ')
            if command.lower().strip() == 'm':
                clear_screen()
                print('Enter message:')
                message = input('~ ')
                print(connection.create_message(user['id'], chat_id, message, user['password_hash']))
                clear_screen()
                chat_messages_menu(chat_id)
            elif commad.lower().strip() == 'b':
                clear_screen()
                logged()
            else:
                chat_messages_menu(chat_id)
    else:
        print('An a server error occured! Try later')
        logged()


def create_message_menu(chat_id):
    user = user_obj.is_logged()['user']
    print('Enter a message (leave blank to go back): ')
    message = input('~ ').strip()
    if len(message) != 0:
        print(connection.create_message(user['id'], chat_id, message, user['password_hash']))
        chat_messages_menu(chat_id)
    else:
        chat_messages_menu(chat_id)
