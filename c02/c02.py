#!/bin/python3
# Bodoki-Halmen Zsolt
# bzim1700
# 531/1

import numpy
from sys import argv

def help(exit_code):
    print('usage: {} input'.format(argv[0]))
    print('\tinput:\tprobabilities of X probability variable, each on a new line')
    print('\t\tthe sum of probabilities should be equal to 1.0')
    exit(exit_code)

class PriorityQueue:
    def __init__(self):
        self.queue = []

    def push(self, leaf):
        if len(self.queue) == 0:
            self.queue.append(leaf)
            return
        index = 0
        while index < len(self.queue) and self.queue[index].prob < leaf.prob:
            index += 1
        if index == len(self.queue):
            self.queue.append(leaf)
            return
        self.queue.insert(index, leaf)

    def pop(self):
        if len(self.queue) == 0:
            return None
        tmp = self.queue[0]
        self.queue[:] = self.queue[1:]
        return tmp

    def empty(self):
        return len(self.queue) == 0

    def size(self):
        return len(self.queue)

class Tree:
    def __init__(self, data=None, leafs=None, huffman_data=None, shannon_fano_data=None):
        def data_to_list(data):
            if isinstance(data, tuple):
                tmp_1 = [data[0]]
                if isinstance(data[0], list):
                    tmp_1 = data[0]
                tmp_2 = [data[1]]
                if isinstance(data[1], list):
                    tmp_2 = data[1]
                return tmp_1 + tmp_2
            else:
                return [data]
        
        self.left = None
        self.right = None
        self.prob = 0.0
        self.data = None

        if huffman_data == None and shannon_fano_data == None:
            if data != None:
                self.prob = data[0]
                self.data = data[1]
            if leafs != None:
                self.left = leafs[0]
                self.right = leafs[1]
                self.prob = leafs[0].prob + leafs[1].prob
                self.data = (data_to_list(leafs[0].data), data_to_list(leafs[1].data))
        elif shannon_fano_data == None:
            self.huffmanFromList(huffman_data)
        else:
            shannon_fano_data.sort(reverse=True)
            root = self.shannonFanoFromList(shannon_fano_data)
            self.left = root.left
            self.right = root.right
            self.prob = root.prob
            self.data = root.data

    def __str__(self):
        def preorder(node, tab):
            if node == None:
                return ''
            string = ''
            i = 0
            while i < tab:
                string += '\t'
                i += 1
            string += str(node.data) + '\n'
            string += preorder(node.left, tab+1) 
            string += preorder(node.right, tab+1)
            return string
        return preorder(self, 0)

    def huffmanFromList(self, huffman_data):
        queue = PriorityQueue()
        for x in huffman_data:
            queue.push(Tree(x))

        while queue.size() > 1:
            t0 = queue.pop()
            t1 = queue.pop()
            t2 = Tree(leafs=(t0, t1))
            queue.push(t2)
        
        root = queue.pop()

        self.left = root.left
        self.right = root.right
        self.prob = root.prob
        self.data = root.data

    def shannonFanoFromList(self, shannon_fano_data):
        def partition(x):
            # x = [(p, e)]
            return [(x[:i], x[i:]) for i in range(1, len(x))]

        def find_best(x):
            #x = [(x0, x1)]
            def keyfunc(x):
                x0, x1 = x
                x0s = 0.0
                for (p,e) in x0:
                    x0s += p
                x1s = 0.0
                for (p, e) in x1:
                    x1s += p
                return abs(x0s - x1s)
            return min(x, key=keyfunc)

        if len(shannon_fano_data) == 1:
            return Tree(data=shannon_fano_data[0])  
        
        xl, xr = find_best(partition(shannon_fano_data))
        left = self.shannonFanoFromList(xl)
        right = self.shannonFanoFromList(xr)
        return Tree(leafs=(left, right))

    def findBinaryCode(self, elem):
        code = None
        node = None
        if elem in self.data[0]:
            code = 0
            node = self.left
        else:
            code = 1
            node = self.right

        while node.data != elem:
            if elem in node.data[0]:
                code *= 2
                node = node.left
            else:
                code *= 2
                code += 1
                node = node.right
        return code

    def findStringCode(self, elem):
        code = ''
        node = None
        if elem in self.data[0]:
            code = '0'
            node = self.left
        else:
            code = '1'
            node = self.right

        while node.data != elem:
            if elem in node.data[0]:
                code += '0'
                node = node.left
            else:
                code += '1'
                node = node.right
        return code

def entropy(x):
    return numpy.sum(x*numpy.log2(1/x))

def average_code_length(x, func):
    E = 0.0
    for (p, e) in x:
        E += p * len(func(e))
    return E

################################################################################

if __name__ == '__main__':
    if len(argv) != 2:
        help(1)
    
    file_name = argv[1]
    f = None
    try:
        f = open(file_name, 'r')
        contents = f.read().strip()
    except:
        help(1)
    finally:
        if f != None:
            f.close()
    
    try:
        x = numpy.array(list(map(float, contents.split('\n'))))
    except ValueError:
        help(1)
    
    if numpy.sum(x) != 1.0:
        help(1)

    H = entropy(x)
    n = range(len(x))

    data = []
    for i in n:
        data.append((x[i], i))

    huffman_tree = Tree(huffman_data=data)
    shannon_fano_tree = Tree(shannon_fano_data=sorted(data, reverse=True))

    E_huffman = average_code_length(data, huffman_tree.findStringCode)
    E_shannon_fano = average_code_length(data, shannon_fano_tree.findStringCode)
    
    print('x entropiaja:\t\t\t\t{}'.format(H))
    print('atlagos huffman kodszohossz:\t\t{:3.2f}'.format(E_huffman))
    print('atlagos shannon-fano kodszohossz:\t{:3.2f}'.format(E_shannon_fano))

    print(shannon_fano_tree)
