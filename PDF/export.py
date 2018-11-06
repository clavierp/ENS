#!/usr/bin/python3

import subprocess
import shutil
import os
import pathlib
import hashlib

EXPORT_COMMAND = 'loffice --headless --convert-to pdf "{}"'


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


def hash(path):
    with open(path, "rb") as f:
        data = f.read()
    return hashlib.sha256(data).hexdigest()


def processDir(root, cache):
    p = pathlib.Path(root)
    files = p.glob("**/*.fodt")
    for f in files:
        full_path = f.as_posix()
        fhash = hash(full_path)
        shash = cache.get(full_path, None)
        print("Exporting {}".format(full_path))
        print("\tFile Hash: {}".format(fhash))
        print("\tSaved Hash:{}".format(shash))
        if shash != fhash:
            export(f)
            cache[full_path] = fhash
        else:
            print("\tSkip")
        print("")


def getCache(cache_file):
    cache = {}
    with open(cache_file) as f:
        for l in f:
            k, v = l.split(":")
            cache[k] = v.replace('\n', '')
    return cache


def saveCache(cache_file, cache):
    with open(cache_file, 'w+') as f:
        for u, v in cache.items():
            print("{}:{}".format(u, v), file=f)


if __name__ == "__main__":
    cache = getCache(".cache")
    processDir("../6", cache)
    processDir("../5", cache)
    saveCache(".cache", cache)
