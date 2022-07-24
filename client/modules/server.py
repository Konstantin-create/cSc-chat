import requests
import json
from loguru import logger
from user import password_hash


class ServerConnection:
    def __init__(self, base_dir):
        self.root = base_dir
        self.server_ip = 'http://127.0.0.1:5000'
    
    # User actions
    # Send login request to server. Responce is get json {'logged': bool}
    def login(self, username, password):
        try:
            response = json.loads(requests.post(
                f'{self.server_ip}/api/user-login',
                json={'login': username, 'password-hash': password_hash(password)}
            ).text)
            return response
        except Exception as e:
            logger.error(e)

    # Send registration request to server. Responce is json {'is_registered': bool}
    def registration(self, login, password):
        try:
            resource = json.loads(requests.post(
                f'{self.server_ip}/api/user-signup',
                json={'login': login, 'password-hash': password_hash(password)}
            ).text)
            return resource
        except Exception as e:
            logger.error(e)
    
    # Check if nickname used by anouther user. Responce is json {'is_free': bool}
    def check_nickname(self, nickname):
        try:
            response = json.loads(requests.get(f'{self.server_ip}/api/check-login/{nickname}').text)
            return response['is_free']
        except Exception as e:
            logger.error(e)

    # Send delete user request to server. Responce is json {'success': bool}
    def delete_user(self, username, password):
        try:
            response = json.loads(requests.post(
                f'{self.server_ip}/api/delete-user', json={'username': username, 'password-hash': password_hash(password)}).text)
            return response
        except Exception as e:
            logger.error(e)
    
    # Chats actions
    # Send create_chat request. Responce is json {'success': bool, 'chat_id': int}
    def create_chat(self, chat_name, chat_creator):
        try:
            response = json.loads(requests.post(
                f'{self.server_ip}/api/create-chat',
                json={'chat_name': chat_name, 'chat_creator': chat_creator}).text)
            return response
        except Exception as e:
            logger.error(e)
    
    # Send delete_chat by name requests. Responce is json {'success': bool}
    def delete_chat_by_name(self, chat_name, chat_creator):
        try:
            response = json.loads(requests.post(
                f'{self.server_ip}/api/remove-chat/by-name',
                json={'chat_name': chat_name, 'chat_creator': chat_creator}).text) 
            return response
        except Exception as e:
            logger.error(e)

    # Send delete_chat by id requests. Responce is json {'success': bool}
    def delete_chat_by_id(self, id, chat_creator):
        try:
            response = json.loads(requests.post(
                f'{self.server_ip}/api/remove-chat/by-id',
                json={'id': id, 'chat_creator': chat_creator}).text)
            return response
        except Exception as e:
            logger.error(e)

    # Send request to get chat info by id. Responce is json {'success': bool, 'chat': {'id': int, 'chat_name': str, 'chat_creator': str}}
    def get_chat_info_by_id(self, id):
        try:
            response = json.loads(requests.get(f'{self.server_ip}/api/get-chat-info/by-id/{id}').text)
            return response
        except Exception as e:
            logger.error(e)
        
    # Send request to get chat info by chat name. Responce is json {'success': bool, 'chat': {'id': int, 'chat_name': str, 'chat_creator': str}}
    def get_chat_info_by_name(self, chat_name):
        try:
            response = json.loads(requests.get(f'{self.server_ip}/api/get-chat-info/by-name/{chat_name}').text)
            return response
        except Exception as e:
            logger.error(e)
    
    # Send request to create message. Response is json {'success': bool, 'message': {'id': int, 'from_user': int, 'from_chat': int, 'body': str, 'time_stamp': obj(datetime)}}
    def create_message(self, from_user, from_chat, body):
        try:
            response = json.loads(requests.post(
                f'{self.server_ip}/api/message/create', json={'body'=body, 'from_user': from_user, 'from_chat': from_chat}).text)
            return response
        except Exception as e:
            logger.error()

    # Send request to get message info. Response is json {'success': bool, 'message': {'id': int, 'from_user': int, 'from_chat': int, 'body': str, 'time_stamp': obj(datetime)}}
    def get_message_info(self, message_id):
        try:
            response = json.loads(requests.get(f'{self.server_ip}/api/message/{message_id}').text)
            return response
        except Exception as e:
            logger.error(e)
    
    # Send request to delete message. Response is json {'success': bool}
    def delete_message(self, message_id):
        try:
            response = json.loads(requests.get(f'{self.server_ip}/api/message/delete/{message_id}').text)
            return response
        except Exception as e:
            logger.error(e)

    # Send request to get all messages from chat id. Response is json {'success': bool, messages: [{'id': int, 'from_user': int, 'from_chat': int, 'body': str, 'time_stamp': obj(datetime)}, ...]}
    def get_chat_messages(self, chat_id):
        try:
            response = json.loads(requests.get(f'{self.server_ip}/api/messages/all/chat-id/{chat_id}').text)
            return response
        except Exception as e:
            logger.error(e)

