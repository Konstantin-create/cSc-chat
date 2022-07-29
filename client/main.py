# Imports
import os
import sys
from config import base_dir
from modules import server, user
from modules import command_handlers


# Functions
def clear_screen():
    if sys.platform == "linux" or sys.platform == "linux2":
        os.system('clear')
    elif sys.platform == "win32":
        os.system('cls')

# Initialize classes
connection = server.ServerConnection(base_dir)
user_obj = user.User(base_dir)

# Main loop
while True:
    if not os.path.exists(f'{base_dir}/cdata/session.session') or len(
            open(f'{base_dir}/cdata/session.session').read()) < 1:
        user_obj.create_session()
    clear_screen()
    if user_obj.is_logged()['logged']:
        command_handlers.logged()
        break
    else:
        command_handlers.not_logged()
