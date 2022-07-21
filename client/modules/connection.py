import json
import os
import requests
from main import logger, User


class ServerConnection(User):
    def __init__(self):
        try:
            self.server_ip = '127.0.0.1:5000'

            self.root_folder, filename = os.path.split(os.path.abspath(__file__))
            self.root_folder = self.root_folder[:self.root_folder.rfind('/')] + '/'
            self.data_path = f'{self.root_folder}/cdata'
            self.downloads_path = f'{self.root_folder}/Downloads'
            self.temp_path = f'{self.root_folder}/temp'
            self.uploads_path = f'{self.temp_path}/uploads'
        except Exception as e:
            logger.error(f'Error: {e}')

    def sign_up(self, login, password):
        try:
            if not self.is_logged():
                query = json.loads(requests.post(login, password).text)['success']
                return query
        except Exception as e:
            logger.error(f'Error: {e}')

    def check_username(self, username):
        try:
            query = json.loads(requests.get(f'http://{self.server_ip}/check-username/{username}').text)['is_free']
            return query
        except Exception as e:
            logger.error(f'Error: {e}')
            return e

    def login(self, login, password):
        try:
            query = requests.get(f'http://{self.server_ip}/api/login').text
            query = json.loads(query)
            return query['logged']
        except Exception as e:
            logger.error(f'Error: {e}')
            return e
