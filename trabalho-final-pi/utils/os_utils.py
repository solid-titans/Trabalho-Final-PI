# This Python file uses the following encoding: utf-8

def folders_in(path_to_parent):
    for file_name in os.listdir(path_to_parent):
        if os.path.isdir(os.path.join(path_to_parent,file_name)):
            yield os.path.join(path_to_parent,file_name)
