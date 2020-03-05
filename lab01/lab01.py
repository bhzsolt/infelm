#!/bin/python3
# Bodoki-Halmen Zsolt
# bzim1700
# 531/1

import re
from sys import argv
from os import listdir
from os import chdir
from math import log2

def increase(dictionary, key):
    if key in dictionary:
        dictionary[key] += 1
    else:
        dictionary[key] = 1

def mutate_dict(func, dictionary):
    for key, value in dictionary.items():
        dictionary[key] = func(value)

def H(X):
    H = 0.0
    for key, p_i in X.items():
        H += p_i * log2(1/p_i)
    return H

def R(H_X, n):
    return 1 - H_X/log2(n)

################################################################################

if len(argv) == 1 or argv[1] not in listdir():
    print('usage: {} language'.format(argv[0]))
    exit(1)

chdir(argv[1])
file_names = listdir()

H1_dict = {}
H2_dict = {}
H3_dict = {}
H1_count = 0
H2_count = 0
H3_count = 0
for file_name in file_names:
    with open(file_name, 'r') as f:
        word_list = list(
                filter(
                    lambda x: x != '', 
                    re.split('\s|[.,:!?\-"]|\d+|\[|\]', f.read().lower())
                    )
                )
    
    for (word_0, word_1, word_2) in zip(word_list, 
                                        word_list[1:], 
                                        word_list[2:]):
        increase(H1_dict, word_0)
        H1_count += 1
        increase(H2_dict, (word_0, word_1))
        H2_count += 1
        increase(H3_dict, (word_0, word_1, word_2))
        H3_count += 1
    increase(H1_dict, word_1)
    increase(H1_dict, word_2)
    H1_count += 2
    increase(H2_dict, (word_1, word_2))
    H2_count += 1

chdir('..')
        
mutate_dict(lambda x: x/H1_count, H1_dict)    
mutate_dict(lambda x: x/H2_count, H2_dict)    
mutate_dict(lambda x: x/H3_count, H3_dict)    

H1 = H(H1_dict)
H2 = H(H2_dict)
H3 = H(H3_dict)
R1 = R(H1, len(H1_dict))
R2 = R(H2, len(H2_dict))
R3 = R(H3, len(H3_dict))

print('1 word entropy for {}:\t{}'.format(argv[1], H1))
print('2 word entropy for {}:\t{}'.format(argv[1], H2/2))
print('3 word entropy for {}:\t{}'.format(argv[1], H3/3))
print('1 word redundancy for {}: \t{}'.format(argv[1], R1))
print('2 word redundancy for {}: \t{}'.format(argv[1], R2*2))
print('3 word redundancy for {}: \t{}'.format(argv[1], R3*3))
