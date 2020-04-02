#!/bin/python3

from math import floor
from sys import argv

def help(exitcode):
    print('usage: {} -hfed'.format(argv[0]))
    print('\t-h\tdisplay this help')
    print('\t-f\tshow binary of fractional')
    print('\t-e\tencode')
    print('\t-d\tdecode')
    print('\t-/\tdivide')
    exit(exitcode)

def binary(x, k):
    string = ''
    while k > 0:
        x *= 2
        string += str(floor(x))
        x -= floor(x)
        k -= 1
    return string

def from_binary(x):
    s = 0.0
    t = 0.5
    for i in range(len(x)):
        if x[i] == '1':
            s += t
        t /= 2
    return s

def find(data, m):
    i0 = 0.0
    for (p, v) in data:
        i1 = i0 + p
        if v == m:
            return (i0, i1)
        i0 = i1

def find2(data, p):
    i0 = 0.0
    for (x, s) in data:
        i1 = i0 + x
        if (i0 < p) and (p <= i1):
            return i0, i1, s
        i0 = i1

def arithmetic_encoder(message, probs):
    i0 = 0.0
    i1 = 1.0
    for m in message:
        p0, p1 = find(probs, m)
        tmp = i0
        i0 = i0 + (i1 - i0) * p0 
        i1 = i0 + (i1 - tmp) * (p1 - p0)
    return i0, i1

def arithmetic_decoder(length, probs, y):
    y += '1'
    c = from_binary(y)
    m = []
    for i in range(length):
        q0, q1, s = find2(probs, c)
        m.append(s)
        c = (c - q0)/(q1 - q0)
    return m

if __name__ == '__main__':
    if len(argv) < 2:
        help(1)
    elif argv[1] == '-h':
        help(0)
    elif argv[1] == '-f':
        f = float(input('enter a floating point number: '))
        print('0.{}'.format(binary(f, 12)))
    elif argv[1] == '-e':
        symbols = input('enter space separated symbols: ').split(' ')
        probs = list(map(float, input('enter space separated probabilities: ').split(' ')))
        message = input('enter space separated message: ').split(' ')
        data = list(zip(probs, symbols))

        i0, i1 = arithmetic_encoder(message, data)
        s0 = binary(i0, 12)
        s1 = binary(i1, 12)
        print(s0, i0)
        print(s1, i1)
    elif argv[1] == '-d':
        length = int(input('enter length: '))
        msg = input('enter message to decode: ')
        symbols = input('enter space separated symbols: ').split(' ')
        probs = list(map(float, input('enter space separated probabilities: ').split(' ')))
        data = list(zip(probs, symbols))
        print(arithmetic_decoder(length, data, msg))
    elif argv[1] == '-/':
        d = int(input('divident: '))
        n = int(input('nominator: '))
        print(d/n)
    else:
        help(1)
