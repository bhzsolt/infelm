#!/usr/bin/python3
# Bodoki-Halmen Zsolt
# bzim1700
# 531/1

import tree as t
import struct as s
from argparse import ArgumentParser
from pathlib import Path

def zero_pad(filename):
    byte = filename.encode()
    n = len(byte)
    if n < 64:
        pad = b'\x00'*(64-n)
        byte += pad
    elif n > 64:
        splitted = filename.split('.')
        extension = splitted[len(splitted) - 1]
        m = 64 - len(extension) - 1
        filename = filename[0:m] + '.' + extension
        byte = filename.encode()
    return byte

def strip_padding(byte):
    return byte.decode().split('\x00')[0]

def loading(verbose, i, n):
    if verbose:
        percent = i/(n - 1)
        current = int(percent*30)
        string = '['
        for x in range(30):
            if x <= current:
                string += '*'
            else:
                string += ' '
        string += ']'
        print(string, end='')
        if i != (n-1):
            print('\b'*32, end='')
        else:
            print()

def log(verbose, message):
    if verbose:
        print(message)

def encode(output_file, input_file, verbose):
    log(verbose, 'encoding {} as {}'.format(input_file, output_file))
    
    root = t.make_tree([i for i in range(256)])
     
    f = open(output_file, 'wb')

    log(verbose, 'encodeing file name')
    f.write(zero_pad(input_file))
    
    log(verbose, 'opening file')
    g = open(input_file, 'rb')
    
    log(verbose, 'encoding')
    i = 0
    n = Path(input_file).stat().st_size
    code = ''
    while True:
        loading(verbose, i, n)
        byte = g.read(1)
        if byte == b'':
            break
        byte = s.unpack('B', byte)[0]
        code += root.encode_character(byte)
        while len(code) >= 8:
            binary = int(code[0:8], 2)
            f.write(s.pack('B', binary))
            code = code[8:]
        i += 1
    g.close()
    if len(code) > 0:
        code += '0'*(8-len(code))
        binary = int(code, 2)
        f.write(s.pack('B', binary))
    f.close()

def decode(input_file, verbose):
    log(verbose, 'decoding {}'.format(input_file))
    
    root = t.make_tree([i for i in range(256)])

    log(verbose, 'opening files')
    f = open(input_file, 'rb')
    filename = strip_padding(f.read(64))
    g = open(filename, 'wb')

    log(verbose, 'decoding')
    i = 0
    n = Path(input_file).stat().st_size
    while True:
        loading(verbose, i, n)
        byte = f.read(1)
        if byte == b'':
            break
        code = '{:08b}'.format(s.unpack('B', byte)[0])
        message = root.decode(code)
        for m in message:
            g.write(s.pack('B', m))
        i += 1
    g.close()
    f.close()

################################################################################

if __name__ == '__main__':
    parser = ArgumentParser(description='Adaptive Huffman Encoder/Decoder')
    parser.add_argument('-d', 
                        '--decode', 
                        nargs=1,
                        metavar='file',
                        help='decode file')
    parser.add_argument('-e', 
                        '--encode', 
                        nargs=2, 
                        metavar='file',
                        help='encode')
    parser.add_argument('-v', 
                        '--verbose', 
                        action='store_true')

    args = parser.parse_args()
    if args.encode == None and args.decode == None:
        parser.parse_args(['-h'])
    elif args.encode != None and args.decode == None:
        encode(args.encode[0], args.encode[1], args.verbose)
    elif args.decode != None and args.encode == None:
        decode(args.decode[0], args.verbose)
