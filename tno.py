#!/home/hymx/fun/tno/venv/bin/python3
from datetime import date
import time
import re
import argparse
import sys
import os
import editor
import json
import subprocess
import pathlib
homeDir = os.path.expanduser("~")
tnoDir = '%s/Documents/tno' % (homeDir)

noteDir = '%s/notes/' % (tnoDir)
noteDB = '%s/tno_db.json' % (tnoDir)


def loadDB():
    global noteDB
    with open(noteDB, 'r') as f:
        db = json.load(f)
    return db


def updateDB(db):
    global noteDB
    with open(noteDB, 'w') as f:
        f.write(json.dumps(db))


def filePathFromName(name):
    global noteDir
    return noteDir + name + '.txt'


def searchNotes(name=None, tags=None, less=True):
    db = loadDB()
    if name in db :
        if less:
            p = subprocess.Popen(["/usr/bin/less", filePathFromName(name)])
            p.wait()
        else:
            with open(filePathFromName(name), 'r') as f:
                print(f.read())
    else:
        print('Note \"{0}\" not found'.format(name))


def listNotes():
    db = loadDB()
    for n in db.keys():
        print(n)


def newNote(name, tags=[]):
    global noteDB
    if len(name) < 1:
        print('Invalid name')
        exit(-1)

    db = loadDB()

    if '/' in name:
        p = noteDir
        for n in name.split('/')[0:-1]:
            p += n + '/'
        if not os.path.isdir(p):
            os.makedirs(p)

    try:
        editor.edit(filePathFromName(name))

        os.path.isfile(filePathFromName(name))
    except:
        return

    db[name] = { 'tags': tags }
    updateDB(db)

def deleteNote(name):
    global noteDir
    try:
        os.remove(filePathFromName(name))
        if '/' in name:
            dirs = name.split('/')[0:-1]
            for i in reversed(range(len(dirs))):
                d = noteDir
                for j in range(i+1):
                    d += dirs[j] + '/'
                if not os.listdir(d):
                    os.rmdir(d)

    except(FileNotFoundError):
        print('File not found')
    db = loadDB()
    if name in db:
        del db[name]
        updateDB(db)


def editNote(name):
    editor.edit(filePathFromName(name))


def validateNoteName(name):
    return not re.search('^([a-z0-9_./])+$', name) is None


def parseArgs():
    parser = argparse.ArgumentParser(description='A terminal based notes app')
    g = parser.add_argument_group('CRUD')
    g.add_argument('-s', '--show', action='store_true', help='Lists all notes')
    g.add_argument('-r', '--read', help='Gets a note by name')
    g.add_argument('-n', '--new', help='Creates new note')
    g.add_argument('-d', '--delete', help='Delete note')
    g.add_argument('-e', '--edit', help='Opens note in your default text editor')
    g.add_argument('-b', '--backup', action='store_true', help='Opens note in your default text editor')
    parser.add_argument('--noless', action='store_true', default=False, help='All output goes to stdout, not less')
    return (parser, parser.parse_args())


def main():
    global noteDir
    parser, args = parseArgs()

    if args.backup:
        t = date.today()
        lt = time.localtime()
        name = t.strftime("%Y-%m-%d-")
        name += '%s-%s-%s' % (lt.tm_hour, lt.tm_min, lt.tm_sec)
        print(name)
        os.system('tar -zcvf ./backup-%s.tar.gz %s' % (name, noteDir))
        return

    if not os.path.isdir(tnoDir):
        os.mkdir(tnoDir)

    if not os.path.isfile(noteDB):
        with open(noteDB, 'w') as f:
            f.write('{}')

    if not os.path.isdir(noteDir):
        os.mkdir(noteDir)


    if args.show:
        listNotes()
    elif args.read != None:
        name = args.read.strip()
        if validateNoteName(name):
            searchNotes(name=name, less=not args.noless)
        else:
            print('Note names must only contain charactors a-z _ .')
    elif args.new != None:
        name = args.new.strip()
        if validateNoteName(name):
            newNote(name)
        else:
            print('Note names must only contain charactors a-z _ .')
    elif args.delete != None:
        name = args.delete.strip()
        if validateNoteName(name):
            deleteNote(name)
        else:
            print('Note names must only contain charactors a-z _ .')
    elif args.edit != None:
        name = args.edit.strip()
        if validateNoteName(name):
            editNote(name)
        else:
            print('Note names must only contain charactors a-z _ .')
    else:
        parser.print_help()



if __name__ == '__main__':
    main()
