from hashlib import sha256


def password_hash(password):
    return sha256(password.encode('utf-8')).hexdigest()


class User:
    def __init__(self, base_dir):
        self.root = base_dir
        self.cdata = f'{self.root}/cdata'

    def get_cdata_session(self):
        with open(f'{self.cdata}/session', 'w') as file:
            session = file.read()
        with open(f'{self.cdata}/chats.json') as file:
            chats = file.read()

