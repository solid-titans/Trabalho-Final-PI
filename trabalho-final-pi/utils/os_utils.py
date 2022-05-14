# This Python file uses the following encoding: utf-8
import os

def folders_in(path_to_parent):
    folders = [ f.path for f in os.scandir(path_to_parent) if f.is_dir() ]
    result = []
    for f in folders:
        result.append(f.split(os.sep)[-1])

    return result
