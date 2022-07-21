import os


def create_base_folders():
    root_folder, filename = os.path.split(os.path.abspath(__file__))
    root_folder = root_folder[:root_folder.rfind('/')] + '/'
    os.mkdir(f'{root_folder}/cdata')
    os.mkdir(f'{root_folder}/temp')
    os.mkdir(f'{root_folder}/temp/uploads')
    os.mkdir(f'{root_folder}/Downloads')
