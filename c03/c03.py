#!/bin/python3
# Bodoki-Halmen Zsolt
# bzim1700
# 531/1

from sys import argv
from os import path
from os import listdir

import tree as t

def help(exitcode):
    print('usage: {} -eh input'.format(argv[0]))
    print('\t-e: encode')
    print('\tinput:\tsource symbols')
    print('\t\tcode symbols')
    print('\t\tsource symbol probabilities')
    print('\t\tmessage to encode')
    print('\t-h: display this help')
    exit(exitcode)

def pre_dir(d):
    def helper(x):
        if d[len(d) - 1] == '/':
            return d + x
        return d + '/' + x
    return helper

def probabilities(probs):
    s = 0.0
    for p in probs:
        s += p
    return s == 1.0

def list_files(args):
    files = list(filter(path.isfile, args))
    folders = list(filter(path.isdir, args))
    i = 0
    while i < len(folders):
        contents = list(map(pre_dir(folders[i]), listdir(folders[i])))
        files += list(filter(path.isfile, contents))
        folders += list(filter(path.isdir, contents))
        i += 1
    return files

def parse_file(file_name):
    with open(file_name, 'r') as f:
        lines = f.read().strip().split('\n')

    elems = lines[0].split(' ')
    probs = [float(x) for x in lines[2].split(' ')]
    symbols = lines[1].split(' ')
    symbols.sort()
    message = lines[3].split(' ')
    return (elems, probs, symbols, message)

################################################################################

if __name__ == '__main__':
    if len(argv) < 2:
        help(1)
    
    if argv[1] == '-h':
        help(0)
    
    if argv[1] != '-e' or (argv[1] == '-e' and len(argv) < 3):
        help(1)

    files = list_files(argv[2:])

    if len(files) == 0:
        print('error: no such file')
        help(1)

    errors = False
    for file_name in files:
        elems, probs, symbols, message = parse_file(file_name)

        if len(elems) != len(probs) or not probabilities(probs):
            print('error: {} not a valid input file'.format(file_name))
            errors = True
            continue
        
        data = []
        for i in range(len(elems)):
            data.append((probs[i], elems[i]))

        tree = t.make_tree(symbols, data)

        print('{}:'.format(file_name))
        print('\tplain message:\t\t', end='')
        for m in message:
            print(m, end='\t')
        print('\n\tencoded message:\t', end='')
        for m in message:
            print(tree.findCode(m), end='\t')
        print('\n\tcodes:')
        E = 0.0
        for (p, e) in data:
            c = tree.findCode(e)
            E += p * len(c)
            print('\t\t{}->{}'.format(e, c))
        print('\tE(|f(X)|) = {:7.4f}'.format(E))
    if errors:
        help(1)
