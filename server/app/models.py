from app import db
from hashlib import sha256


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)

    def check_password(self, password):
        if self.password_hash == sha256(password.encode('utf-8')):
            return True

    def __repr__(self):
        return '<User %r>' % self.username
