#!/bin/python3

from functools import reduce

def create_indexes(length):
    a = length // 8
    if length / 8 - a >= 0.5:
        a += 1
    x = []
    for i in range(7):
        x.append((a*i, a*(i+1)))
    x.append((a*7, length))
    return x

def printlist(l):
    for (a,b) in create_indexes(len(l)):
        print('{:2d}:{:2d} -> {}'.format(a,b,l[a:b]))

def explode(s):
    if s == "what's":
        return ['what', 'is']
    if s == "hasn't":
        return ['has', 'not']
    if s == "haven't":
        return ['have', 'not']
    if s == "shouldn't":
        return ['should', 'not']
    if s == "wouldn't":
        return ['would', 'not']
    if s == "couldn't":
        return ['could', 'not']
    if s == "aren't":
        return ['are', 'not']
    if s == "wasn't":
        return ['was', 'not']
    if s == "it's":
        return ['it', 'is']
    return [s]

rewrite = lambda xs: reduce(lambda out, cur: out + explode(cur), xs, [])
