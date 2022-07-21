from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////databases/users.db'
db = SQLAlchemy(app)

from modules import models

if __name__ == '__main__':
    from modules.routes import *
    app.run()
