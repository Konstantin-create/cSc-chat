import os
from modules import server

base_dir = os.path.abspath(os.path.dirname(__file__))

connection = server.ServerConnection(base_dir)
