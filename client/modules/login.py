import os
import json
import datetime
from hashlib import sha256
from main import logger


class User:
    # Init app paths
    def __init__(self):
        self.root_folder, filename = os.path.split(os.path.abspath(__file__))
        self.root_folder = self.root_folder[:self.root_folder.rfind('/')] + '/'
        self.data_path = f'{self.root_folder}/cdata'

    # Check is user logged(session file)
    def is_logged(self):
        try:
            with open(f'{self.data_path}/session', 'r') as file:
                file_len = len(file.read())
        except Exception as e:
            logger.warning(f'Warning: {e}')
        if os.path.exists(f'{self.data_path}/session') and file_len != 0:
            return True
        return False

    # Create session file where store username, password-hash and login date
    def new_login(self, login, password):
        if not self.is_logged():
            try:
                password_hash = sha256(password.encode('utf-8')).hexdigest()
                with open(f'{self.data_path}/session', 'w') as file:
                    json.dump(
                        {'login': login, 'password-hash': password_hash, 'login-time': str(datetime.datetime.now())},
                        file
                    )
            except Exception as e:
                logger.error(f'Error: {e}')
                return False
            return True
        return False

    # Logout clear session file
    def logout(self):
        if self.is_logged():
            with open(f'{self.data_path}/session', 'w') as file:
                file.write('')
