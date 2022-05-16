# This Python file uses the following encoding: utf-8
import os
import shutil
import tempfile

def folders_in(path_to_parent):
    folders = [ f.path for f in os.scandir(path_to_parent) if f.is_dir() ]
    result = []
    for f in folders:
        result.append(f.split(os.sep)[-1])

    return result

def get_user_home():
    return os.path.expanduser('~')

def get_os_tmp_path():
    return tempfile.gettempdir()

def create_folder(folder_path):

    if(not os.path.exists(folder_path)):
        os.mkdir(folder_path)
    else:

        """
        Make the folder empty
        """
        for root, dirs, files in os.walk(folder_path):
            for f in files:
                os.unlink(os.path.join(root, f))
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))

def join_paths(path1,path2):
    return os.path.join(path1,path2)