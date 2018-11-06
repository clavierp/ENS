#!/usr/bin/python3

import subprocess
import shutil
import os
import pathlib
import hashlib
import logging
import io

EXPORT_COMMAND = 'loffice --headless --convert-to pdf "{}"'
RED = "\033[31m{}\033[0m"
GREEN = "\033[32m{}\033[0m"
BLUE = "\033[34m{}\033[0m"


def getname(path):
    pathFull = path.as_posix()
    parts = pathFull.split('/')
    return " - ".join(parts[1:])


def export(filein, targetdir='.'):
    name = getname(filein)
    shutil.copyfile(filein.as_posix(), targetdir+"/"+name)
    logging.info("\tCOPY[OK]")
    p = subprocess.Popen(EXPORT_COMMAND.format(name), shell=True, stdout=subprocess.PIPE)
    out = p.communicate()[0]
    p.wait()
    if(len(out) != 0):
        logging.info("\tEXPORT[OK]")
        status = 0
    else:
        logging.warning("\tEXPORT[FAIL]: office already started")
        status = 1
    os.remove(targetdir+'/'+name)
    logging.info("\tCLEAN[OK]")
    return status


def hash(path):
    with open(path, "rb") as f:
        data = f.read()
    return hashlib.sha256(data).hexdigest()


def processDir(root, cache):
    p = pathlib.Path(root)
    files = p.glob("**/*.fodt")
    for f in files:
        full_path = f.as_posix()
        print("{} [    ]".format(full_path), end='', flush=True)
        status = 0
        fhash = hash(full_path)
        shash = cache.get(full_path, None)
        logging.info("Exporting {}".format(full_path))
        logging.info("\tFile Hash: {}".format(fhash))
        logging.info("\tSaved Hash:{}".format(shash))
        if shash != fhash:
            status = export(f)
            if status == 0: cache[full_path] = fhash
        else:
            logging.info("\tSkip")
            status = 2
        if status == 0: print("\b\b\b\b\b"+GREEN.format(" OK ")+"]")
        if status == 1: print("\b\b\b\b\b"+RED.format("FAIL")+"]")
        if status == 2: print("\b\b\b\b\b"+BLUE.format("SKIP")+"]")

def getCache(cache_file):
    cache = {}
    try:
        with open(cache_file, "r+") as f:
            for l in f:
                k, v = l.split(":")
                cache[k] = v.replace('\n', '')
    except FileNotFoundError:
        logging.warning("Cache file not found")
    return cache


def saveCache(cache_file, cache):
    with open(cache_file, 'w+') as f:
        for u, v in cache.items():
            print("{}:{}".format(u, v), file=f)


if __name__ == "__main__":
    logging.basicConfig(filename="export.log", level=logging.DEBUG)
    cache = getCache(".cache")
    processDir("../6", cache)
    processDir("../5", cache)
    saveCache(".cache", cache)
