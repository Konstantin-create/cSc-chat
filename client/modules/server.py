import sys
import requests
import json
from loguru import logger
from modules.user import password_hash


class ServerConnection:
    def __init__(self, base_dir):
        self.root = base_dir
        self.server_ip = 'http://127.0.0.1:5000'

    # User actions
    """'success': False, when server error happend, so in that case other dict values became None.
    In other cases 'success': True"""

    def login(self, username: str, password: str):
        """Login function get username and password params.
            Return dict {'success': bool, 'logged': bool}"""
        try:
            response = json.loads(requests.post(
                f'{self.server_ip}/api/user-login',
                json={'username': username, 'password-hash': password_hash(password)}
            ).text)
            return response
        except requests.exceptions.ConnectionError:
            logger.error('No internet connection! Try later')
            sys.exit()
        except Exception as e:
            logger.error(e)

    def registration(self, username: str, password: str):
        """Registration function get username and password params.
            Return dict {'success: bool, 'is_registered': bool}"""
        try:
            resource = json.loads(requests.post(
                f'{self.server_ip}/api/user-signup',
                json={'username': username, 'password-hash': password_hash(password)}
            ).text)
            return resource
        except requests.exceptions.ConnectionError:
            logger.error('No internet connection! Try later')
            sys.exit()
        except Exception as e:
            logger.error(e)

    def check_nickname(self, username: str):
        """Check if nickname used by anouther user function. Get username param.
            Return dict {'success': bool, 'is_free': bool}"""
        try:
            response = json.loads(requests.get(f'{self.server_ip}/api/check-login/{username}').text)
            return response
        except requests.exceptions.ConnectionError:
            logger.error('No internet connection! Try later')
            sys.exit()
        except Exception as e:
            logger.error(e)

    def check_session(self, id: int, username: str, password_hash: str):
        """Function to check cdata/session.session data. Get id, username, password_hash.
            Return dict {'success': bool, 'logged': bool}"""
        try:
            response = json.loads(requests.post(
                f'{self.server_ip}/api/check-session',
                json={'id': id, 'username': username, 'password_hash': password_hash}).text)
            return response
        except requests.exceptions.ConnectionError:
            logger.error('No internet connection! Try later')
            sys.exit()
        except Exception as e:
            logger.error(e)

    def get_id_by_username(self, username, password):
        """Get user id by username function. Get username and password params.
            Return dict {'success': bool, 'user_id': int}"""
        try:
            response = json.loads(requests.post(
                f'{self.server_ip}/api/get-user-id/by-username',
                json={'username': username, 'password-hash': password_hash(password)}).text)
            return response
        except requests.exceptions.ConnectionError:
            logger.error('No internet connection! Try later')
            sys.exit()
        except Exception as e:
            logger.error(e)

    def delete_user(self, username: str, password_hash: str):
        """Delete user function. Get username and password_hash params.
            Return dict {'success': bool, 'deleted': bool}"""
        try:
            response = json.loads(requests.post(
                f'{self.server_ip}/api/delete-user',
                json={'username': username, 'password-hash': password_hash}).text)
            return response
        except requests.exceptions.ConnectionError:
            logger.error('No internet connection! Try later')
            sys.exit()
        except Exception as e:
            logger.error(e)

    # Chats actions
    def create_chat(self, chat_name: str, chat_creator_id: int, password_hash: str):
        """Create chat function. Get chat_name, chat_creator and chat creator password_hash params.
            Return dict {'success': bool, 'chat_id': int}"""
        try:
            response = json.loads(requests.post(
                f'{self.server_ip}/api/create-chat',
                json={'chat_name': chat_name, 'chat_creator_id': chat_creator_id, 'password-hash': password_hash}).text)
            return response
        except requests.exceptions.ConnectionError:
            logger.error('No internet connection! Try later')
            sys.exit()
        except Exception as e:
            logger.error(e)

    def delete_chat_by_name(self, chat_name: str, chat_creator: int, password: str):
        """Delete chat by chat name function. Get chat name, chat_creator password, params.
            Return dict {'success': bool', 'deleted': bool}"""
        try:
            response = json.loads(requests.post(
                f'{self.server_ip}/api/remove-chat/by-name',
                json={'chat_name': chat_name, 'chat_creator_id': chat_creator,
                      'password-hash': password_hash(password)}).text)
            return response
        except requests.exceptions.ConnectionError:
            logger.error('No internet connection! Try later')
            sys.exit()
        except Exception as e:
            logger.error(e)

    def delete_chat_by_id(self, id: int, chat_creator_id: int, password: str):
        """Delete chat by id function. Get id(chat_id), chat_creator_id, password params.
            Return dict {'success': bool, 'deleted': bool}"""
        try:
            response = json.loads(requests.post(
                f'{self.server_ip}/api/remove-chat/by-id',
                json={'id': id, 'chat_creator_id': chat_creator_id, 'password-hash': password_hash(password)}).text)
            return response
        except requests.exceptions.ConnectionError:
            logger.error('No internet connection! Try later')
            sys.exit()
        except Exception as e:
            logger.error(e)

    def get_chat_info_by_id(self, chat_id: id):
        """Get chat info by id function. Get chat_id param.
            Return dict {'success': bool, 'chat': {'id': int, 'chat_name': str, 'chat_creator': str}}"""
        try:
            response = json.loads(requests.get(f'{self.server_ip}/api/get-chat-info/by-id/{chat_id}').text)
            return response
        except requests.exceptions.ConnectionError:
            logger.error('No internet connection! Try later')
            sys.exit()
        except Exception as e:
            logger.error(e)

    def get_chat_info_by_name(self, chat_name: str):
        """Get chat info by chat_name function. Get chat_name param.
            Return dict {'success': bool, 'chat': {'id': int, 'chat_name': str, 'chat_creator': str}}"""
        try:
            response = json.loads(requests.get(f'{self.server_ip}/api/get-chat-info/by-name/{chat_name}').text)
            return response
        except requests.exceptions.ConnectionError:
            logger.error('No internet connection! Try later')
            sys.exit()
        except Exception as e:
            logger.error(e)

    def get_user_chats(self, user_id):
        """Function to get user chats by id. Get user_id param. Return dict {'success': bool, 'chats': list}"""
        try:
            response = json.loads(requests.get(f'{self.server_ip}/api/get-users-chat/{user_id}').text)
            return response
        except requests.exceptions.ConnectionError:
            logger.error('No internet connection! Try later')
            sys.exit()
        except Exception as e:
            logger.error(e)

    # Message actions
    def create_message(self, from_user: id, from_chat: id, body: str, password):
        """Create message function. Get from_user, from_chat, body, password params.
            Return dict {'success': bool, 'message': {'id': int, 'from_user': int, 'from_chat': int,
            'body': str, 'time_stamp': obj(datetime)}}"""
        try:
            response = json.loads(requests.post(
                f'{self.server_ip}/api/message/create',
                json={'body': body, 'from_user': from_user, 'from_chat': from_chat,
                      'password-hash': password_hash(password)}).text)
            return response
        except requests.exceptions.ConnectionError:
            logger.error('No internet connection! Try later')
            sys.exit()
        except Exception as e:
            logger.error(e)

    def get_message_info(self, message_id, user_id, password):
        """Get message info. Get message_id, user_id, password params.
            Return dict {'success': bool, 'message': {'id': int, 'from_user': int, 'from_chat': int,
            'body': str, 'time_stamp': obj(datetime)}}"""
        try:
            response = json.loads(requests.post(f'{self.server_ip}/api/message/info',
                                                json={'message_id': message_id, 'user_id': user_id,
                                                      'password-hash': password_hash(password)}).text)
            return response
        except requests.exceptions.ConnectionError:
            logger.error('No internet connection! Try later')
            sys.exit()
        except Exception as e:
            logger.error(e)

    def delete_message(self, message_id: int, user_id, password):
        """Delete message function. Get message_id param. Return dict {'success': bool, 'deleted': bool}"""
        try:
            response = json.loads(requests.post(f'{self.server_ip}/api/message/delete',
                                                json={'message_id': message_id, 'user_id': user_id,
                                                      'password-hash': password_hash(password)}).text)
            return response
        except requests.exceptions.ConnectionError:
            logger.error('No internet connection! Try later')
            sys.exit()
        except Exception as e:
            logger.error(e)

    def get_chat_messages(self, chat_id: int):
        """Get all chat messages. Get chat_id param.
        Return dict {'success': bool, messages: [{'id': int, 'from_user': int, 'from_chat': int,
            'body': str, 'time_stamp': obj(datetime)}, ...]}"""
        try:
            response = json.loads(requests.get(f'{self.server_ip}/api/messages/all/chat-id/{chat_id}').text)
            return response
        except requests.exceptions.ConnectionError:
            logger.error('No internet connection! Try later')
            sys.exit()
        except Exception as e:
            logger.error(e)

    # User subscriptions actions
    def subscribe_chat(self, chat_id, current_user_id, password_hash):
        """Function to add user subscription. Get chat_id, current_user_id, password_hash params.
        Return dict {'success': bool, 'added': bool}"""
        try:
            response_check_id = self.get_chat_info_by_id(chat_id)
            if response_check_id['chat']:
                if response_check_id['chat']['chat_creator_id'] == current_user_id:
                    print('U are already in this chat!')
                    print()
                else:
                    response = json.loads(requests.post(
                        f'{self.server_ip}/api/user-subscriptions/add',
                        json={'user_id': current_user_id, 'password_hash': password_hash, 'chat_id': chat_id}).text)
                    return response
        except requests.exceptions.ConnectionError:
            logger.error('No internet connection! Try later')
            sys.exit()
        except Exception as e:
            logger.error(e)

    def get_user_subscriptions(self, current_user_id, password_hash):
        """Function to get user subscriptions"""
        try:
            response = json.loads(requests.post(
                f'{self.server_ip}/api/user-subscriptions/get',
                json={'user_id': current_user_id, 'password_hash': password_hash}).text)
            return response
        except requests.exceptions.ConnectionError:
            logger.error('No internet connection! Try later')
            sys.exit()
        except Exception as e:
            logger.error(e)

    def unsubscribe_chat(self, chat_id, current_user_id, password_hash):
        """Function to remove user subscription. Get chat_id, current_user_id, password_hash params.
        Return dict {'success': bool, 'deleted': bool}"""
        try:
            response_check_id = self.get_chat_info_by_id(chat_id)
            if response_check_id['chat']:
                if response_check_id['chat']['chat_creator_id'] == current_user_id:
                    print('U cant unsubscribe our own chat!')
                    print()
                else:
                    response = json.loads(requests.post(
                        f'{self.server_ip}/api/user-subscription/delete',
                        json={'user_id': current_user_id, 'password_hash': password_hash, 'chat_id': chat_id}).text)
                    return response
        except requests.exceptions.ConnectionError:
            logger.error('No internet connection! Try later')
            sys.exit()
        except Exception as e:
            logger.error(e)
