#!/usr/bin/env python3

import re
import argparse
import sys
import os
import editor
import json

noteDB = './tno_db.json'
noteDir = 'notes/'


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


def searchNotes(name=None, tags=None):
    db = loadDB()
    try:
        for o in db:
            if o['name'] == name:
                with open(filePathFromName(name), 'r') as f:
                    print(f.read())
    except(Exception):
        print('Note \"{0}\" not found'.format(name))


def listNotes():
    db = loadDB()
    for n in db:
        print(n['name'])


def newNote(name, tags=[]):
    global noteDB
    if len(name) < 1:
        print('Invalid name')
        exit(-1)
    db = loadDB()
    db.append({ 'name': name, 'tags': tags })
    updateDB(db)
    editor.edit(filePathFromName(name))


def deleteNote(name):
    try:
        os.remove(filePathFromName(name))
    except(Exception):
        pass
    updateDB( list( filter( lambda x: x['name'] != name, loadDB() ) ) )


def editNote(name):
    editor.edit(filePathFromName(name))


def validateNoteName(name):
    return not re.search('^([a-z,_,.])+$', name) is None


def parseArgs():
    parser = argparse.ArgumentParser(description='A terminal based notes app')
    parser.add_argument('-s', '--show', required=False, action='store_true', help='Lists all notes')
    parser.add_argument('-r', '--read', required=False, help='Gets a note by name')
    parser.add_argument('-n', '--new', required=False, help='Creates new note')
    parser.add_argument('-d', '--delete', required=False, help='Delete note')
    parser.add_argument('-e', '--edit', required=False, help='Opens note in your default text editor')
    return parser.parse_args()


def main():
    args = parseArgs()

    if args.show:
        listNotes()
    elif args.read != None:
        name = args.read.strip()
        if validateNoteName(name):
            searchNotes(name=name)
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




if __name__ == '__main__':
    main()
