from app import db
from modules.models import User

db.create_all()

guest = User(username='guest', password_hash='5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8')
db.session.add(guest)
db.session.commit()
