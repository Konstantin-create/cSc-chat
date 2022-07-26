import os
import json
from loguru import logger
from hashlib import sha256
from datetime import datetime



def password_hash(password):
    return sha256(password.encode('utf-8')).hexdigest()


class User:
    def __init__(self, base_dir: str):
        self.root = base_dir
        self.cdata = f'{self.root}/cdata'
        self.base_session = {'user': {'id': None, 'username': None, 'password_hash': None}}
    
    # Working with files
    def get_cdata(self):
        """Function to get all data from cdata folder. Return dict {'session': dict, 'chats': list}"""
        try:
            session = None
            chats = None
            if os.path.exists(f'{self.cdata}/session.session'):
                with open(f'{self.cdata}/session.session', 'r') as file:
                    session = json.load(file)
            if os.path.exists(f'{self.cdata}/chats.json'):
                with open(f'{self.cdata}/chats.json', 'r') as file:
                    chats = json.load(file)
            return {'session': session, 'chats': chats}
        except Exception as e:
            logger.error(e)
            return {'session': None, 'chats': None}
    
    def set_chats(self, chat_list: list):
        """Function to set chat list. Get chat_list param. Return dict {'recorded': bool}"""
        try:
            with open(f'{self.cdata}/chats.json', 'w') as file:
                json.dump(chat_list, file)
            return {'recorded': True}
        except Exception as e:
            logger.error(e)
            return {'recorded', False}

    def add_chat_to_chats(chat: dict):
        try:
            current_chats = self.get_cdata()['chats']
            if current_chats is None:
                self.set_chats([chat])
                return {'added': True}
            current_chats.append(chat)
            self.set_chats(current_chats)
            return {'added': True}
            pass # todo добавление алемента в список чатов.
        except Exception as e:
            logger.error(e)
            return {'added': False}
    
    def create_session(self):
        """Function to create empty session file"""
        try:
            with open(f'{self.cdata}/session.session', 'w') as file:
                json.dump(self.base_session, file)
            return {'created': True}
        except Exception as e:
            logger.error(e)
            return {'creted': False}

    def set_session(self, session: dict):
        """Function to write info in session file. Get session(dict) param. Return dict {'recorded': bool}"""
        try:
            with open(f'{self.cdata}/session.session', 'w') as file:
                json.dump(session, file)
            return {'recorded': True}
        except Exception as e:
            logger.error(e)
            return {'recorded': False}

    # Login/registration routes
    def is_logged(self):
        """Function to read cdata/session.session and get user data from threre. Return dict {'logged': bool, 'user': dict}"""
        # try:
        if os.path.exists(self.cdata) and os.path.exists(f'{self.cdata}/session.session'):
            session = self.get_cdata()['session']
            if session['user']['username'] or session['user']['password_hash']:
                return {'logged': True, 'user': session['user']}
        return {'logged': False, 'user': None}
        # except Exception as e:
        #     logger.error(e)
        #     return {'logged': False, 'user': None}

    def login(self, user_id, username, password):
        """Function to write userdata in session file. Get username, password params. Return dict {'logged': bool, 'user': dict}"""
        try:
            user = {'id': user_id, 'username': username, 'password_hash': password_hash(password), 'login_time': datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')}
            print(user)
            session = self.get_cdata()['session']
            session['user'] = user
            self.set_session(session)
            return {'logged': True, 'user': user}
        except Exception as e:
            logger.error(e)
            return {'logged': False}

    def logout(self, username, password):
        """Function to logout user. Get username, password params. Return dict {'logout': bool}"""
        try:
            session = self.get_cdata()['session']
            if 'user' in session:
                if session['user']['username'] == username and session['user']['password'] == password_hash(password):
                    del session['user']
                else:
                    logger.warning('Wrong username or password')
                    return {'logout': False}
            return {'logout': True}
        except Exception as e:
            logger.error(e)
            return {'logout': False}

    # Chat functions
    def delete_chat(self, chat_id):
        """Function to delete chat by id. Get chat id param. Return dict {'deleted': bool}"""
        try:
            chats = self.get_cdata()
            for chat in chats:
                if chat['id'] == chat_id:
                    del chat
                    return {'deleted': True}
        except Exception as e:
            logger.error(e)
            return {'deleted': False}

    # Messages functions
    def get_all_messages(self):
        """Function to get all saved messages. Return dict {'messages': dict}"""
        try:
            with open(f'{self.root}/cdata/messages.json', 'r') as file:
                messages = json.load(file)
            return {'messages': messages}
        except Exception as e:
            logger.error(e)
            return {'messages': None}

    def get_chat_messages(self, chat_id):
        """Function to get saved messages by chat id. Get chat id param. Return dict {'messages': list}"""
        try:
            all_messages = self.get_all_messages()
            if chat_id in all_messages:
                return {'messages', all_messages[chat_id]}
            return {'messages': []}
        except Exception as e:
            logger.error(e)
            return {'messages': None}

    def delete_chat_message(self, chat_id, message_id):
        """Function to delete chat by chat id. Return dict {'deleted': bool}"""
        try:
            messages = self.get_all_messages()
            del messages[chat_id][message_id]
        except Exception as e:
            logger.error(e)
            return {'deleted': None}

