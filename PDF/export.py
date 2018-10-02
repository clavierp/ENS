#!/usr/bin/python3

import subprocess
import shutil
import os

EXPORT_COMMAND = "loffice --headless --convert-to pdf '{}'"

def getname(path):
    parts = path.split("/")
    return " - ".join(parts[-3:])


def export(filein, targetdir='.'):
    print("Processing {}: ".format(filein), end='')
    name = getname(filein)
    print("new name = {} ".format(name), end='')
    shutil.copyfile(filein, targetdir+"/"+name)
    print(" COPY ", end='')
    subprocess.Popen(EXPORT_COMMAND.format(name), shell=True).wait()
    print(" TRANFORM ", end='')
    os.remove(targetdir+'/'+name)
    print(" REMOVE {} ".format(targetdir+'/'+name))

def processDir(root):
    files = os.walk(root)
    res = []
    for f in files:
        for g in f[2]:
            res.append(f[0]+'/'+g)
    print(res)
    files = [f for f in res if f[-5:] == ".fodt"]

    for f in files:
        export(f)

if __name__=="__main__":
    processDir("../6")
    processDir("../5")

