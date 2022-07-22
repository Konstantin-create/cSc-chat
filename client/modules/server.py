import requests
import json
from loguru import logger
from user import password_hash


class ServerConnection:
    def __init__(self, base_dir):
        self.root = base_dir
        self.server_ip = 'http://127.0.0.1:5000'

    # Send login request to server and get json {'logged': bool}
    def login(self, username, password):
        try:
            response = json.loads(requests.post(
                f'{self.server_ip}/api/user-login',
                json={'login': username, 'password-hash': password_hash(password)}
            ).text)
            return response
        except Exception as e:
            logger.error(e)

    # Send registration request to server and get json {'is_registered': bool}
    def registration(self, login, password):
        try:
            resource = json.loads(requests.post(
                f'{self.server_ip}/api/user-signup',
                json={'login': login, 'password-hash': password_hash(password)}
            ).text)
            return resource
        except Exception as e:
            logger.error(e)
    
    # Check if nickname used by anouther user. Return json {'is_free': bool}
    def check_nickname(self, nickname):
        try:
            response = json.loads(requests.get(f'{self.server_ip}/api/check-login/{nickname}').text)
            return response['is_free']
        except Exception as e:
            logger.error(e)

    # Send delete user request to server. Get json {'success': bool}
    def delete_user(self, username):
        try:
            response = json.loads(requests.post(
                f'{self.server_ip}/api/delete-user', json={'username': username}).text)
            return response
        except Exception as e:
            logger.error(e)


server = ServerConnection('/home/hacknet/Kostua/Python/cSc-chat/client')
print(server.registration('guest', 'password'))
print(server.delete_user('guest'))
