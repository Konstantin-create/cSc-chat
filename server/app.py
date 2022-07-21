from flask import Flask

app = Flask(__name__)

from modules.routes import *

if __name__ == '__main__':
    app.run()
