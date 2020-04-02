#!/bin/python3
# Bodoki-Halmen Zsolt
# bzim1700
# 531/1

import random
from sys import argv
from tree import Tree

def average_code_length(x, func):
    E = 0.0
    for (p, e) in x:
        E += p * len(func(e))
    return E

def generate_probabilities(n):
    while True:
        probs = []
        s = 1.0
        for i in range(n-1):
            p = random.uniform(0,1)
            probs.append(p)
            s -= p
        if s > 0:
            probs.append(s)
            break
    return probs

################################################################################

if __name__ == '__main__':
    random.seed()
    book = {True: 0, False: 0}
    for i in range(10**4): 
        n = random.randint(3,4)
        probs = generate_probabilities(n)
        data = list(zip(probs, range(n)))

        huffman_tree = Tree(huffman_data=data)
        shannon_fano_tree = Tree(shannon_fano_data=sorted(data, reverse=True))

        E_huffman = average_code_length(data, huffman_tree.findStringCode)
        E_shannon_fano = average_code_length(data, shannon_fano_tree.findStringCode) 
        book[abs(E_huffman - E_shannon_fano) < 0.000001] += 1
    
    print('E(Huffman) == E(Shannon-Fano):', book)
