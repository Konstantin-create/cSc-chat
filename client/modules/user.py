import json
from loguru import logger
from hashlib import sha256


def password_hash(password):
    return sha256(password.encode('utf-8')).hexdigest()


class User:
    def __init__(self, base_dir: str):
        self.root = base_dir
        self.cdata = f'{self.root}/cdata'
    
    # Working with files
    def get_cdata(self):
        """Function to get all data from cdata folder. Return dict {'session': dict, 'chats': list}"""
        try:
            with open(f'{self.cdata}/session.session', 'r') as file:
                session = json.load(file)
            with open(f'{self.cdata}/chats.json', 'r') as file:
                chats = json.load(file)
            return {'session': session, 'chats': chats}
        except Exception as e:
            logger.error(e)
            return {'session': None, 'chats': None}
    
    def set_chats(self, chat_list: list):
        """Function to set chat list. Get chat_list param. Return dict {'recorded': bool}"""
        try:
            with open(f'{self.cdata}/chats', 'w') as file:
                json.dump(chat_list, file)
            return {'recorded': True}
        except Exception as e:
            logger.error(e)
            return {'recorded', False}
    
    def set_session(self, session: dict):
        """Function to write info in session file. Get session(dict) param. Return dict {'recorded': bool}"""
        try:
            with open(f'{self.cdata}/session', 'w') as file:
                json.dump(session, file)
            return recorded
        except Exception as e:
            logger.error(e)
            return {'recorded': False}

    def change_session_key(self, key:str, value: any):
        """Function to change some sesssion values in file. Get key, value params. Return dict {'recorded': bool}"""
        try:
            session = get_cdata()['session']
            session[key] = value
            set_session(session)
        except Exception as e:
            logger.error(e)
            return {'recorded': False}

