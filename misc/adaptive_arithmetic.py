#!/usr/bin/python3

import numpy as np
from sys import argv
from math import floor

class AdaptiveArithmeticEncoder:
    def __init__(self, X, EOM):
        self.X = [*X, EOM]
        self.EOM = EOM
        self.n = len(self.X)
        self.p = np.array([1 for x in range(self.n)])
        self.i = [0.0, 1.0]
    
    def init_q(p):
        return np.array([ p[0:i].sum() for i in range(len(p) + 1) ])

    def find_in_symbols(self, s):
        for i in range(self.n):
            if s == self.X[i]:
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
    
    def encode(self, symbol):
        p = self.p/self.n
        q0 = AdaptiveArithmeticEncoder.init_q(p)
        
        q = self.i[0] + (self.i[1] - self.i[0]) * q0
        s = self.find_in_symbols(symbol)
        self.i[0] = q[s]
        self.i[1] = q[s + 1]

        #print('{}:\t{} -> {}'.format(AdaptiveArithmeticEncoder.stringify(q), symbol, self.i))

        self.p[s] += 1
        self.n += 1
        return tuple(self.i)
    
    def decode(self, i):
        c = (i[0] + i[1]) / 2
        print(c)
        message = []
        while True:
            p = self.p/self.n
            q = AdaptiveArithmeticEncoder.init_q(p)
            s = AdaptiveArithmeticEncoder.find_in_interval(q, c)
            c = (c - q[s]) / (q[s + 1] - q[s])
            message.append(self.X[s])
            if self.X[s] == self.EOM:
                break
            self.p[s] += 1
            self.n += 1
        return message

    #erroneous
    def decode_from_binary(self, binary):
        binary += '1'
        c = from_binary(binary)
        print(c)
        message = []
        while True:
            p = self.p/self.n
            q = AdaptiveArithmeticEncoder.init_q(p)
            s = AdaptiveArithmeticEncoder.find_in_interval(q, c)
            c = (c - q[s]) / (q[s + 1] - q[s])
            message.append(self.X[s])
            if self.X[s] == self.EOM:
                break
            self.p[s] += 1
            self.n += 1
        return message

def binary(x, k):
    string = ''
    while k > 0 and x < 1.0:
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

################################################################################

if __name__ == '__main__':
    symbols = input('Enter space separated symbols: ').split(' ')
    EOM = input('Enter end of message symbol: ').strip()
    encoder = AdaptiveArithmeticEncoder(symbols, EOM)
    decoder = AdaptiveArithmeticEncoder(symbols, EOM)
    
    while True:
        s = input('Enter next symbol: ')
        i = encoder.encode(s)
        if s == EOM:
            break
    n = 128
    b = [binary(i[0], n), binary(i[1], n)]
    m = ''
    x = 0
    while x < n and b[0][x] == b[1][x]:
        m += b[0][x]
        x += 1
    print('Code: {} -> {}'.format(m, i))
    
    message = decoder.decode(i)
    print('The message: {}'.format(message))
    print('From binary: {}'.format(decoder.decode_from_binary(m)))
