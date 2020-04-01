#!/usr/bin/env python3

import re
import argparse
import sys
import os
import editor
import json
import subprocess
import pathlib

noteDB = str(pathlib.Path(__file__).parent.absolute()) + '/tno_db.json'
noteDir = str(pathlib.Path(__file__).parent.absolute()) + '/notes/'

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
    db[name] = { 'tags': tags }
    updateDB(db)
    if '/' in name:
        p = noteDir
        for n in name.split('/')[0:-1]:
            p += n + '/'
        if not os.path.isdir(p):
            os.makedirs(p)

    editor.edit(filePathFromName(name))


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
    g.add_argument('-s', '--show', required=False, action='store_true', help='Lists all notes')
    g.add_argument('-r', '--read', required=False, help='Gets a note by name')
    g.add_argument('-n', '--new', required=False, help='Creates new note')
    g.add_argument('-d', '--delete', required=False, help='Delete note')
    g.add_argument('-e', '--edit', required=False, help='Opens note in your default text editor')
    parser.add_argument('--noless', action='store_true', default=False, help='All output goes to stdout, not less')
    return (parser, parser.parse_args())


def main():
    parser, args = parseArgs()
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
