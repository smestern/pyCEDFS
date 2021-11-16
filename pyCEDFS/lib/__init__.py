import os
import sys


def is_64bit():
    return sys.maxsize > 2**32

def get_dllpath():
    libpath = os.path.abspath(os.path.dirname(__file__))
    if is_64bit():
        dllname = "CFS64.dll"
    else:
        dllname = "CFS32.dll"
    return os.path.join(libpath, dllname)
