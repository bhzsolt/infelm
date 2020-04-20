#!/usr/bin/python3

import numpy as np
from sys import argv

def init_q(p):
    return np.array([ p[0:i].sum() for i in range(len(p)+1) ])
    
def find_in_symbols(X, m):
    for i in range(len(X)):
        if m == X[i]:
            return i
    
def find_in_interval(q, c):
    s = 0
    while s < (len(q) - 1):
        if (q[s] < c) and (c <= q[s + 1]):
            return s
        s += 1

def stringify(q):
    string = '[{:5.3f}'.format(q[0])
    for x in q[1:]:
        string += ',\t{:5.3f}'.format(x)
    string += ']'
    return string

def encode(X, p, u):
    q0 = init_q(p)
    i0 = 0.0
    i1 = 1.0
    for m in u:
        q = i0 + (i1 - i0) * q0
        s = find_in_symbols(X, m)
        i0 = q[s]
        i1 = q[s+1]
        print('{}:\t{} -> {}'.format(stringify(q), m, (i0,i1)))

    return i0, i1

def decode(X, p, k, i0, i1):
    q0 = init_q(p)
    c = (i0 + i1) / 2
    i0 = 0.0
    i1 = 1.0
    message = []
    for _ in range(k):
        q = i0 + (i1 - i0) * q0
        s = find_in_interval(q, c)
        message.append(X[s])
        i0 = q[s]
        i1 = q[s + 1]
    return message

def decode2(X, p, k, i0, i1):
    q = init_q(p)
    c = (i0 + i1) / 2
    message = []
    for _ in range(k):
        s = find_in_interval(q, c)
        c = (c - q[s]) / (q[s + 1] - q[s])
        message.append(X[s])
    return message

def help(exitcode):
    print('usage: {} -hed'.format(argv[0]))
    print('\t-h: display this help')
    print('\t-e: encode')
    print('\t-d: decode')
    exit(exitcode)

################################################################################

if __name__ == '__main__':
    if len(argv) < 2:
        help(1)

    if argv[1] == '-e' or argv[1] == '-d':
        X = input('Enter space separated symbols: ').split(' ')
        p = np.array(list(map(float, input('Enter space separated probabilities: ').split(' '))))

        if argv[1] == '-e':
            u = input('Enter space separated message: ').split(' ')
            print(encode(X, p, u))
            exit(0)

        k = int(input('Enter the length of the message: '))
        i0, i1 = tuple(map(float, input('Enter space separated (i0, i1]: ').split(' ')))
        print(decode(X, p, k, i0, i1))
        print(decode2(X, p, k, i0, i1))
        exit(0)
    elif argv[1] == '-h':
        help(0)
    
    help(1)

