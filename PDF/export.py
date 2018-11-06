#!/usr/bin/python3

import subprocess
import shutil
import os
import pathlib

EXPORT_COMMAND = "loffice --headless --convert-to pdf '{}'"


def getname(path):
    pathFull = path.as_posix()
    parts = pathFull.split('/')
    return " - ".join(parts[1:])


def export(filein, targetdir='.'):
    name = getname(filein)
    shutil.copyfile(filein.as_posix(), targetdir+"/"+name)
    print("\tCOPY[OK]")
    subprocess.Popen(EXPORT_COMMAND.format(name), shell=True).wait()
    print("\tEXPORT[OK]")
    os.remove(targetdir+'/'+name)
    print("\tCLEAN[OK]")


def processDir(root):
    p = pathlib.Path(root)
    files = p.glob("**/*.fodt")
    for f in files:
        print("Exporting {}".format(f.as_posix()))
        export(f)
        print("\n")


if __name__ == "__main__":
    processDir("../6")
    processDir("../5")
