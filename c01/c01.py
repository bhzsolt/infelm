#!/bin/python3
# Bodoki-Halmen Zsolt
# bzim1700
# 531/1

from sys import argv
from os import path
from math import log2

def error():
    print('usage: {} prob_file'.format(argv[0]))
    exit(1)

def prob(p):
    return 0.0 <= p and p <= 1.0

def interp_arg():
    if len(argv) < 2:
        error()

    file_name = argv[1]
    if not path.isfile(file_name):
        print('{} is not a file'.format(file_name))
        error()

    with open(file_name, 'r') as f:
        lines = f.read().strip().split('\n')

    px = float(lines[0])
    py0 = float(lines[1])
    py1 = float(lines[2])

    if len(lines) != 3 or not prob(px) or not prob(py0) or not prob(py1):
        print('{} not a valid prob_file'.format(file_name))
        error()

    return px, py0, py1

def entropy(A):
    return A[0] * log2(1 / A[0]) + A[1] * log2(1 / A[1])

def cond_entropy_x(A, x):
    return A[x][0] * log2(1 / A[x][0]) + A[x][1] * log2(1 / A[x][1])

def cond_entropy(A, B):
    return B[0] * cond_entropy_x(A, 0) + B[1] * cond_entropy_x(A, 1)

def mutual_prob(A, B, a, b):
    return A[b][a] * B[b]

def mutual_entropy(A, B):
    H = 0.0
    for x in range(2):
        for y in range(2):
            H += mutual_prob(A, B, x, y) * log2(1 / mutual_prob(A, B, x, y))
    return H

def relative_entropy(A, B):
    return A[0] * log2(A[0] / B[0]) + A[1] * log2(A[1] / B[1])

def mutual_information(A_, A, B):
    I = 0.0
    for x in range(2):
        for y in range(2):
            I += mutual_prob(A_, B, x, y) * log2(mutual_prob(A_, B, x, y) / (A[x] * B[y]))
    return I

################################################################################

if __name__ == '__main__': 
    px, py0, py1 = interp_arg()
    py = py0 * (1-px) + py1 * px

    X = (1-px, px)
    Y = (1-py, py)

    Y0 = (1-py0, py0)
    Y1 = (1-py1, py1)
    Y_ = (Y0, Y1)

    px0 = mutual_prob(Y_, X, 0, 1)/Y[0]
    px1 = mutual_prob(Y_, X, 1, 1)/Y[1]

    X0 = (1-px0, px0)
    X1 = (1-px1, px1)
    X_ = (X0, X1)

    print('H(X)\t= {:8.6f}'.format(entropy(X)))
    print('H(Y)\t= {:8.6f}'.format(entropy(Y)))
    print('H(X,Y)\t= {:8.6f}'.format(mutual_entropy(Y_, X)))
    #print('H(X,Y)\t= {:8.6f}'.format(cond_entropy(X_, Y)+cond_entropy(Y_, X)+mutual_information(Y_, Y, X)))
    print('H(X|Y)\t= {:8.6f}'.format(cond_entropy(X_, Y)))
    print('H(Y|X)\t= {:8.6f}'.format(cond_entropy(Y_, X)))
    #print('H(Y|X)\t= {:8.6f}'.format(entropy(Y)-mutual_information(Y_, Y, X)))
    #print('H(Y|X)\t= {:8.6f}'.format(mutual_entropy(Y_, X)-entropy(X)))
    print('I(X,Y)\t= {:8.6f}'.format(mutual_information(Y_, Y, X)))
    #print('I(Y,X)\t= {:8.6f}'.format(mutual_information(X_, X, Y)))
    print('D(X||Y)\t= {:8.6f}'.format(relative_entropy(X, Y)))
    print('D(Y||X)\t= {:8.6f}'.format(relative_entropy(Y, X)))
