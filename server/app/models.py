from app import db
from datetime import datetime
from hashlib import sha256


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

    def check_password(self, password):
        if self.password_hash == sha256(password.encode('utf-8')):
            return True

    def __repr__(self):
        return f'<User {self.username}>'


class Chat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chat_name = db.Column(db.String(80), unique=True, nullable=False)

    def __repr__(self):
        return f'<Chat {self.id}>'


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    from_user = db.Column(db.Integer, db.ForeignKey('user.id'))
    from_chat = db.Column(db.Integer, db.ForeignKey('chat.id'))
    time_stamp = db.Column(db.DateTime, index=True, default=datetime.utcnow())

    def __repr__(self):
        return f'<Message | Chat: {self.from_chat} | User: {self.from_user}>'
