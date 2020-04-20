#!/usr/bin/python3
# Bodoki-Halmen Zsolt
# bzim1700
# 531/1

import string
import struct as s
from argparse import ArgumentParser

class Node:
    def __init__(self, n):
        self.n = n
        self.children = {}

class Trie:
    def __init__(self, labels=None):
        self.n = 0
        self.current = 0
        self.children = {}

        if labels != None:
            self.set_children(labels)
    
    def set_children(self, labels):
        for label in labels:
            self.current += 1
            node = Node(self.current)
            self.children[label] = node

    def encode(self, functions, message):
        transform, write = functions
        i = 0
        n = len(message)
        node = self
        while i < n:
            if message[i] in node.children:
                node = node.children[message[i]]
                i += 1
            else:
                write(transform(node.n))
                self.current += 1
                child = Node(self.current)
                node.children[message[i]] = child
                node = self
        write(transform(node.n))

    def encode_without_buffer(self, transform, fetch, write):
        node = self
        char = fetch(1)
        while True:
            if char == '':
                break
            elif char in node.children:
                node = node.children[char]
                char = fetch(1)
            else:
                write(transform(node.n))
                self.current += 1
                node.children[char] = Node(self.current)
                node = self
        write(transform(node.n))

    def encode_binary_without_buffer(self, transform, fetch, write):
        node = self
        byte = fetch(1)
        while True:
            if byte == b'':
                break
            else:
                char = s.unpack('B', byte)[0]
                if char in node.children:
                    node = node.children[char]
                    byte = fetch(1)
                else:
                    write(transform(node.n))
                    self.current += 1
                    node.children[char] = Node(self.current)
                    node = self
        write(transform(node.n))

    def find_label(self, code):
        def helper(node, code):
            if node.n == code:
                return []
            for label, child in node.children.items():
                string = helper(child, code)
                if string != None:
                    return [label] + string
        return helper(self, code)
    
    def find_node(self, string):
        i = 0
        n = len(string)
        node = self
        while i < n:
            node = node.children[string[i]]
            i += 1
        return node
    
    def decode(self, functions, code):
        transform = functions[0]
        write = functions[1]

        n = len(code)
        string = self.find_label(code[0])
        for s in string:
            write(transform(s))
        node = self.find_node(string)
        i = 1
        while i < n:
            string = self.find_label(code[i])
            self.current += 1
            node.children[string[0]] = Node(self.current)
            node = self.find_node(string)
            for s in string:
                write(transform(s))
            i += 1

    def decode_without_buffer(self, transform, fetch, write):
        string = self.find_label(int(fetch().strip()))
        for s in string:
            write(transform(s))
        node = self.find_node(string)
        inp = fetch().strip()
        while True:
            try:
                n = int(inp)
            except ValueError:
                return inp
            string = self.find_label(n)
            self.current += 1
            node.children[string[0]] = Node(self.current)
            node = self.find_node(string)
            for s in string:
                write(transform(s))
            inp = fetch().strip()
    
    def decode_binary_without_buffer(self, transform, fetch, write):
        byte = fetch(2)
        if byte == b'':
            return
        n = s.unpack('H', byte)[0]
        if n == 0:
            return
        string = self.find_label(n)
        for x in string:
            write(transform(x))
        node = self.find_node(string)
        byte = fetch(2)
        while True:
            if byte == b'': 
                return
            n = s.unpack('H', byte)[0]
            if n == 0:
                return
            string = self.find_label(n)
            self.current += 1
            node.children[string[0]] = Node(self.current)
            node = self.find_node(string)
            for x in string:
                write(transform(x))
            byte = fetch(2)

def create_parser():
    parser = ArgumentParser(description='LZW Encoder/Decoder')
    parser.add_argument('-b',
                        '--binary',
                        action='store_true',
                        help='binary encoding/decoding')
    parser.add_argument('-i',
                        '--interactive',
                        action='store_true',
                        help='interactive encoding/decoding')
    parser.add_argument('-d',
                        '--decode',
                        nargs='*',
                        metavar='file',
                        help='decode file')
    parser.add_argument('-e',
                        '--encode',
                        nargs='*',
                        metavar='file',
                        help='encode output file(s)')
    return parser
    
def dictionary(_list):
    _dict = {}
    for e in _list:
        if e in _dict:
            _dict[e] += 1
        else:
            _dict[e] = 1
    return list(_dict.keys())

def interactive_encode():
    text = input('Enter text to encode:\n')
    labels = dictionary(text)
    trie = Trie(labels)
    trie.encode([lambda n: n, print], text)

def interactive_decode():
    alphabet = input('Enter space separated alphabet: ').split(' ')
    trie = Trie(alphabet)
    print('Enter code, terminate with newline:')
    code = []
    while True:
        n = input()
        if n == '':
            break
        n = int(n)
        code.append(n)
    trie.decode([lambda c: c, lambda c: print(c, end='')], code)
    print()

def not_binary_encode(output_file, input_files):
    alphabet = list(string.printable)
    f = open(output_file, 'w')
    for _file in input_files:
        f.write(_file + '\n')
        trie = Trie(alphabet)
        g = open(_file, 'r')
        trie.encode_without_buffer(lambda n: '{}\n'.format(n), g.read, f.write)
        g.close()
    f.close()

def not_binary_decode(input_file):
    f = open(input_file, 'r')
    g = None
    n = None
    filename = None
    trie = None
    alphabet = list(string.printable)
    filename = f.readline().strip()
    g = open(filename, 'w')
    while True:
        trie = Trie(alphabet)
        filename = trie.decode_without_buffer(lambda x: x, f.readline, g.write)
        g.close()
        if filename != '':
            g = open(filename, 'w')
        else:
            break

def zero_pad(filename):
    byte = filename.encode()
    n = len(byte)
    if n % 2 != 0:
        byte += b'\x00'
    return byte

def strip_padding(byte):
    return byte.decode().split('\x00')[0]

def binary_encode(output_file, input_files):
    alphabet = [i for i in range(256)]
    f = open(output_file, 'wb')
    for _file in input_files:
        f.write(zero_pad(_file))
        f.write(s.pack('H', 0))
        trie = Trie(alphabet)
        g = open(_file, 'rb')
        trie.encode_binary_without_buffer(lambda n: s.pack('H', n), g.read, f.write)
        g.close()
        f.write(s.pack('H', 0))
    f.close()

def binary_decode(input_file):
    alphabet = [i for i in range(256)]
    f = open(input_file, 'rb')
    while True:
        byte = b''
        quit = False
        while True:
            next_byte = f.read(2)
            if next_byte == b'':
                quit = True
                break
            elif s.unpack('H', next_byte)[0] != 0:
                byte += next_byte
            else:
                break
        if not quit:
            filename = strip_padding(byte)
            trie = Trie(alphabet)
            g = open(filename, 'wb')
            trie.decode_binary_without_buffer(lambda n: s.pack('B', n), f.read, g.write)
            g.close()
        else:
            break

################################################################################

if __name__ == '__main__':
    parser = create_parser()
    args = parser.parse_args()
    
    decode_flag = args.decode != None and args.encode == None
    encode_flag = args.encode != None and args.decode == None
    interactive_flag = args.interactive and not args.binary
    binary_flag = args.binary and not args.interactive

    if not decode_flag and not encode_flag:
        parser.parse_args(['-h'])
    if interactive_flag:
        if encode_flag:
            interactive_encode()
        elif decode_flag:
            interactive_decode()
    elif not binary_flag:
        if encode_flag:
            if len(args.encode) < 2:
                print('no input file')
                parser.parse_args(['-h'])
            not_binary_encode(args.encode[0], args.encode[1:])
        elif decode_flag:
            if len(args.decode) < 1:
                print('no input file')
                parser.parse_args(['-h'])
            not_binary_decode(args.decode[0])
    elif binary_flag:
        if encode_flag:
            if len(args.encode) < 2:
                print('no input file')
                parser.parse_args(['-h'])
            binary_encode(args.encode[0], args.encode[1:])
        elif decode_flag:
            if len(args.decode) < 1:
                print('no input file')
                parser.parse_args(['-h'])
            binary_decode(args.decode[0])

