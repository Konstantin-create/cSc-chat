# Imports
import os
from modules import server, user

# Initialize root dir path
base_dir = os.path.abspath(os.path.dirname(__file__))

# Initialize classes
connection = server.ServerConnection(base_dir)
user = user.User(base_dir)


# Main loop
while True:
    pass

