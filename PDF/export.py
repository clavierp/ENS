#!/usr/bin/python3

import pathlib
import shutil
import subprocess


def getname(path):
    pathFull = path.as_posix()
    parts = pathFull.split('/')
    return " - ".join(parts[1:])

def copy(filein, targetdir='.'):
    name = getname(filein)
    shutil.copyfile(filein.as_posix(), targetdir+'/'+name)
    

def processDir(root):
    p = pathlib.Path(root)
    files = p.glob("**/*.pdf")
    for f in files:
        full_path = p.as_posix()
        copy(f)

if __name__=="__main__":
    processDir("../6")
