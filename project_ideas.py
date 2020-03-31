#!/usr/bin/env python3

import argparse
import sys
import os

projFile = "./project_ideas.txt"



def getProjData(projName):
    global projFile
    with open(projFile, 'r') as f:
        for p in list(map(lambda x: x.replace('\n', '').split(','), f.readlines())):
            if p[0] == projName:
                return (p[0].strip(), p[1].strip())
        return (None, None)


def desc(projName):
    (name, descFile) = getProjData(projName)
    if name is None or descFile is None:
        print('The project {0} was not found, check: project_ideas --list')
        exit(-1)

    if not os.path.exists('desc/{0}'.format(descFile)):
        _ = createProjDesc(name)

    with open(descFile) as f:
        print(f.read())


def listProjs():
    global projFile
    with open(projFile, 'r') as f:
        for p in list( map( lambda x: x.split(',')[0], f.readlines() ) ):
            print(p)

def newProjIdea(name):
    global projFile
    if len(name) < 3:
        print('Invalid name')
        exit(-1)
    desc = createProjDesc(name)
    with open(projFile, 'a') as f:
        f.write("{0},{1}\n".format(name, desc))

def createProjDesc(name):
    descPath = 'desc/' + name.replace(' ', '_').split('.')[0] + '_outline' + '.txt'
    with open('desc/' + name.replace(' ', '_').split('.')[0] + '_outline' + '.txt', 'w') as f:
        f.write(name)
    return descPath

def parseArgs():
    parser = argparse.ArgumentParser(description='A data-bank of project ideas')
    parser.add_argument('--list', action='store_true', help='Lists all project ideas')
    parser.add_argument('--outline', help='Gets project outline by name')
    parser.add_argument('--new', help='Creates new project idea')
    return parser.parse_args()


def main():
    args = parseArgs()

    if args.list:
        listProjs()
    elif args.outline != None:
        desc(args.outline.strip())
    elif args.new != None:
        newProjIdea(args.new.strip())



if __name__ == '__main__':
    main()
