#!/usr/bin/python3
# Bodoki-Halmen Zsolt
# bzim1700
# 531/1

import parse as p
import struct as s
from argparse import ArgumentParser


class Node:
    def __init__(self, n):
        self.n = n
        self.children = {}

class Trie:
    def __init__(self):
        # counter for current highest index
        self.n = 0
        self.current = 0
        # dictionary of {data: node}
        self.children = {}
     
    def encode(self, message):
        i = 0
        n = len(message)
        reset = True
        not_printed = True
        code = []
        while i < n:
            if reset:
                node = self
                reset = False
            d = None; _n = None
            for td, tn in node.children.items():
                if td == message[i]:
                    d = td
                    _n = tn
                    break
            if d != None:
                node = _n
                not_printed = True
            else:
                code.append((node.n, message[i]))
                self.current += 1
                child = Node(self.current)
                node.children[message[i]] = child
                reset = True
                not_printed = False
            i += 1
        if not_printed:
            print(type(message[i-1]), '::', type(message[i-1])(1))
            code.append((node.n, type(message[i-1])(1)))
        return code

    def decode(self, codes):
        def find(node, number):
            if node.n == number:
                return []
            for label, child in node.children.items():
                string = find(child, number)
                if string != None:
                    return [label] + string
        
        def insert(node, labels, number, label):
            i = 0
            n = len(labels)
            while i < n:
                for d, _n in node.children.items():
                    if d == labels[i]:
                        node = _n
                        i += 1
                        break
            child = Node(number)
            node.children[label] = child

        message = []
        for number, char in codes:
            if number < self.current:
                labels = find(self, number)
                message += labels + [char]
                self.current += 1
                insert(self, labels, self.current, char)
            else:
                message += [char]
                self.current += 1
                child = Node(self.current)
                self.children[char] = child
        return message

def zero_pad(filename):
    byte = filename.encode()
    n = len(byte)
    if n < 64:
        pad = b'\x00'*(64-n)
    byte += pad
    return byte

def strip_padding(byte):
    return byte.decode().split('\x00')[0]

def decode(binary, input_file):
    if binary:
        with open(input_file, 'rb') as f:
            while True:
                filename = strip_padding(f.read(64))
                if filename == '':
                    break
                n = s.unpack('H', f.read(2))[0]
                code = []
                for _ in range(n):
                    number = s.unpack('H', f.read(2))[0]
                    char = s.unpack('B', f.read(1))[0]
                    code.append((number, char))
                trie = Trie()
                message = trie.decode(code)
                if message[len(message) - 1] == type(message[0])(1):
                    message.pop()
                with open(filename, 'wb') as g:
                    for m in message:
                        g.write(s.pack('B', m))
    else:
        with open(input_file, 'r') as f:
            while True:
                filename = f.readline().strip()
                if filename == '':
                    break
                n = int(f.readline().strip())
                code = []
                for _ in range(n):
                    n, c = p.parse('({:d}, {})', f.readline().strip()).fixed
                    if c == '\\n':
                        c = '\n'
                    code.append((n, c))
                trie = Trie()
                message = trie.decode(code)
                if message[len(message) - 1] in ['-', '\x00']:
                    message[len(message) - 1] = '\n'
                with open(filename, 'w') as g:
                    for m in message:
                        g.write(m)

def encode(binary, input_files):
    output_file = input_files[0]
    if binary:
        f = open(output_file, 'wb')
        for _file in input_files[1:]:
            with open(_file, 'rb') as g:
                contents = g.read()
            trie = Trie()
            code = trie.encode(contents)
            f.write(zero_pad(_file))
            f.write(s.pack('H', len(code)))
            for n, c in code:
                f.write(s.pack('HB', n, c))
        f.close()
    else:
        f = open(output_file, 'w')
        for _file in input_files[1:]:
            with open(_file, 'r') as g:
                contents = g.read()
            trie = Trie()
            code = trie.encode(contents)
            f.write(_file + '\n')
            f.write(str(len(code)) + '\n')
            for n, c in code:
                if c == '\n':
                    c = '\\n'
                f.write('({}, {})\n'.format(n, c))
        f.close()

################################################################################

if __name__ == '__main__':
    parser = ArgumentParser(description='LZ78 Encoder/Decoder')
    parser.add_argument('-b',
                        '--binary',
                        action='store_true',
                        help='binary encoding/decoding')
    parser.add_argument('-d', 
                        '--decode',
                        nargs=1,
                        metavar='file',
                        help='decode file')
    parser.add_argument('-e',
                        '--encode',
                        nargs='+',
                        metavar='file',
                        help='encode output file(s)')
    
    args = parser.parse_args()
    if args.decode == None and args.encode == None:
        args = parser.parse_args(['-h'])
    if args.decode != None:
        decode(args.binary, args.decode[0])
    if args.encode != None:
        encode(args.binary, args.encode)

