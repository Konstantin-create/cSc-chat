from hashlib import sha256


def password_hash(password):
    return sha256(password.encode('utf-8')).hexdigest()


class User:
    def __init__(self, base_dir):
        self.root = base_dir
