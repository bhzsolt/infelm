#!/bin/python3

def partition(x):
    # x = [(p, e)]
    return [(x[:i], x[i:]) for i in range(1, len(x))]

def find_best(x):
    #x = [(x0, x1)]
    def keyfunc(x):
        x0, x1 = x
        x0s = 0.0
        x1s = 0.0
        for (p,e) in x0:
            x0s += p
        for (p, e) in x1:
            x1s += p
        return abs(x0s - x1s)
    return min(x, key=keyfunc)

#__init__(self, data=None, leafs=None, huffman_data=None, shannon_fano_data=None):
def makeFromList(shannon_fano_data):
    if len(shannon_fano_data) == 1:
        return Tree(data=shannon_fano_data[0])  
    
    xl, xr = find_best(partition(shannon_fano_data))
    left = makeFromList(xl)
    right = makeFromList(xr)
    return Tree(leafs=(left, right))

