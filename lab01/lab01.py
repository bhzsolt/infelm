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

if __name__ == '__main__':

    if len(argv) == 2 and argv[1] not in listdir():
        print('usage: {} language'.format(argv[0]))
        exit(1)
    elif len(argv) == 1:
        languages = listdir()
        to_remove_list = ['test.py', 'lab01.py', '__pycache__', '.gitignore']
        for to_remove in to_remove_list:
            languages.remove(to_remove)
    else:
        languages = argv[1:]

    for language in languages:
        chdir(language)
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
                            re.split('\s|[.,;:!?\-"()]|\d+|\[|\]', f.read().lower())
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
        H2 = H(H2_dict)/2
        H3 = H(H3_dict)/3
        R1 = R(H1, len(H1_dict))
        R2 = R(H2, len(H2_dict))
        R3 = R(H3, len(H3_dict))

        print(language)
        print('{} words'.format(len(H1_dict)))
        print('\tentropy:\t{}'.format(H1))
        print('\tredundancy:\t{}'.format(R1))
        print('{} bigramms'.format(len(H2_dict)))
        print('\tentropy:\t{}'.format(H2))
        print('\tredundancy:\t{}'.format(R2))
        print('{} trigramms'.format(len(H3_dict)))
        print('\tentropy:\t{}'.format(H3))
        print('\tredundancy:\t{}'.format(R3))
        print()

