#!/bin/python3
# Bodoki-Halmen Zsolt
# bzim1700
# 531/1

import struct
from sys import argv
from math import log2

def error():
    print('usage: {} -e/d input'.format(argv[0]))
    print('\t-e: encode')
    print('\t-d: decode')
    exit(1)

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
    def __init__(self, data=None, leafs=None, datalist=None):
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
        if datalist == None:
            if data != None:
                self.prob = data[0]
                self.data = data[1]
            if leafs != None:
                self.left = leafs[0]
                self.right = leafs[1]
                self.prob = leafs[0].prob + leafs[1].prob
                self.data = (data_to_list(leafs[0].data), data_to_list(leafs[1].data))
        else:
            self.fromList(datalist)

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

    def fromList(self, data):
        queue = PriorityQueue()
        for x in data:
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

def encode(input_file):
    output_file = input_file + '.hm'
    with open(input_file, 'rb') as f:
        raw = f.read()

    dictionary = {}
    for i in raw:
        if i in dictionary:
            dictionary[i] += 1
        else:
            dictionary[i] = 1

    data = list(map(lambda x: (x[1]/len(raw), x[0]), dictionary.items()))
    tree = Tree(datalist=data)

    encoded_file_name = input_file.encode()
    n = len(encoded_file_name)
    if n < 64:
        encoded_file_name += bytes(64 - n)
    elif n > 64:
        split = input_file.split('.')
        fext = '.' + split[len(split)-1]
        encoded_fext = fext.encode()
        m = len(encoded_fext)
        encoded_file_name = encoded_file_name[:(64 - n - m)] + encoded_fext

    encoded_string = ''
    for i in raw:
        encoded_string += tree.findStringCode(i)
    
    n = len(encoded_string) % 8
    if n != 0:
        encoded_string += '0' * (8 - n)

    data.sort(key=lambda x: x[1])
    with open(output_file, 'wb') as f:
        f.write(encoded_file_name)
        for (p, e) in data:
            f.write(struct.pack('f', p))
        for i in range(0, len(encoded_string), 8):
            f.write(struct.pack('B', int(encoded_string[i:i+8], 2)))

def decode(input_file):
    with open(input_file, 'rb') as f:
        filename = f.read(64)
        probdata = f.read(1024)
        stream = f.read()

    output_file = bytes.decode(filename).split('\x00')[0]

    data = []
    for e in range(256):
        p = struct.unpack('f', probdata[e*4:e*4+4])[0]
        data.append((p, e))
    tree = Tree(datalist=data)

    decoded_string = ''
    for i in stream:
        decoded_string += '{:08b}'.format(i)

    i = 0
    decoded_data = []
    n = len(decoded_string)
    while i < n:
        node = tree
        while isinstance(node.data, tuple):
            if decoded_string[i] == '0':
                node = node.left
            elif decoded_string[i] == '1':
                node = node.right
            i += 1
        decoded_data.append(node.data)
        if (n - i) <= 8:
            if decoded_string[i:] == ('0' * (n - i)):
                break

    with open(output_file, 'wb') as f:
        for e in decoded_data:
            f.write(struct.pack('B', e))


################################################################################

if len(argv) < 3:
    error()

if argv[1] == '-e':
    encode(argv[2])
    exit(0)
elif argv[1] == '-d':
    decode(argv[2])
    exit(0)

error()
