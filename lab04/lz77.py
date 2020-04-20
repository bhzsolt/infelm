#!/usr/bin/python3
# Bodoki-Halmen Zsolt
# bzim1700
# 531/1

import struct as s
import parse as p
from pathlib import Path
from argparse import ArgumentParser

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

def to_bytes(offset, length, next_char):
    if next_char == '-':
        next_char = ord(next_char)
    return s.pack('BBB', offset, length, next_char)

def to_tuple(offset, length, next_char):
    if next_char == '\n':
        next_char = '\\n'
    return '<{}, {}, {}>\n'.format(offset, length, next_char)

# swl -> search window length
# lawl -> lookahead window length
def encode_without_overflow(functions, message, swl=None, lawl=None):
    def find_prefix(search, lookahead):
        length = 0; offset = 0; char = None
        match_index = 0
        n = len(lookahead)
        m = len(search)
        while (match_index < m) and (lookahead[0] != search[match_index]):
            match_index += 1
        if match_index < m:
            while (length < n) and ((length + match_index) < m) and (
                        lookahead[length] == search[match_index + length]):
                length += 1
            offset = m - match_index
        if length < n:
            char = lookahead[length]
        return (offset, length, char)
    
    if swl == None:
        swl = 8
    if lawl == None:
        lawl = 3
    code = functions[0]
    write = functions[1]
    i = 0
    n = len(message)
    while i < n:
        offset, length, next_char = find_prefix(message[max(0, i-swl):i], message[i:(i+lawl)])
        if next_char == None:
            if (i+length) < n:
                next_char = message[i+length]
            else:
                next_char = '-'
        write(code(offset, length, next_char))
        i += length + 1

# swl -> search window length
# lawl -> lookahead window length
def encode_with_overflow(functions, message, swl=None, lawl=None):
    if swl == None:
        swl = 8
    if lawl == None:
        lawl = 3
    code = functions[0]
    write = functions[1]

    i = 0
    n = len(message)
    # i -> index of search window | lookahead window
    while i < n:
        length = 0; offset = 0; next_char = None
        match_index = 0;
        sb = max(0, i - swl)
        se = lb = i
        le = min(n, lb + lawl)
        # finding first match from search window with first char of lookahead
        while (match_index < (se - sb)) and (message[sb:se][match_index] != 
                                       message[lb:le][0]):
            match_index += 1
        # if match was found
        if match_index < (se - sb):
            # calculate length
            while (length < (le - lb)) and (message[sb + match_index + length] ==
                                  message[lb:le][length]):
                length += 1
            # finding offset
            offset = (se - sb) - match_index
            # finding next char
            if (i + length) < n:
                next_char = message[i + length]
            else:
                next_char = '-'
        # setting the next char to its right value
        if next_char == None:
            if (i + length) < n:
                next_char = message[i + length]
            else:
                next_char = '-'
        write(code(offset, length, next_char))
        i += length + 1
    return code

def decode(code):
    message = []
    i = 0
    for offset, length, next_char in code:
        if next_char == '\\n':
            next_char = '\n'
        for x in range(length):
            message += [message[i-offset+x]]
        message += [next_char]
        i += length + 1
    return message

def interactive_encode(overflow):
    text = input('Enter text to be encoded: ')
    if overflow:
        encode_with_overflow([to_tuple, lambda x: print(x, end='')], text, 256, 64)
    else:
        encode_without_overflow([to_tuple, lambda x: print(x, end='')], text, 256, 64)

def interactive_decode():
    code = []
    print('enter codes <{:d}, {:d}, {}>, terminate with a newline:')
    while True:
        inp = input()
        if inp == '':
            break
        code.append(p.parse('<{:d}, {:d}, {}>', inp.strip()).fixed)
    msg = decode(code)
    message = ''
    for m in msg:
        message += m
    print('The decoded message is:', message)

def not_binary_encode(overflow, output_file, input_files):
    f = open(output_file, 'w')
    for _file in input_files:
        f.write(_file + '\n')
        with open(_file, 'r') as g:
            text = g.read()
        if overflow:
            encode_with_overflow([to_tuple, f.write], text, 256, 64)
        else:
            encode_without_overflow([to_tuple, f.write], text, 256, 64)
        f.write('\n')
    f.close()

def not_binary_decode(input_file):
    with open(input_file, 'r') as f:
        contents = f.read().split('\n')
    i = 0
    n = len(contents)
    while i < n:
        filename = contents[i]
        if filename != '':
            code = []
            i += 1
            while i < n and contents[i] != '':
                code.append(p.parse('<{:d}, {:d}, {}>', contents[i]).fixed)
                i += 1
            msg = decode(code)
            message = ''
            for m in msg:
                message += m
            with open(filename, 'w') as g:
                g.write(message)
        i += 1

def binary_encode(overflow, output_file, input_files):
    f = open(output_file, 'wb')
    for _file in input_files:
        f.write(zero_pad(_file))
        with open(_file, 'rb') as g:
            text = g.read()
        text = [i for i in text]
        if overflow:
            encode_with_overflow([to_bytes, f.write], text, 128, 32)
        else:
            encode_without_overflow([to_bytes, f.write], text, 128, 32)
        f.write(s.pack('B', 255))
    f.close()

def binary_decode(input_file):
    f = open(input_file, 'rb')
    while True:
        byte = f.read(64)
        if byte == b'':
            break
        filename = strip_padding(byte)
        g = open(filename, 'wb')
        code = []
        while True:
            offset = s.unpack('B', f.read(1))[0]
            if offset == 255:
                break
            length = s.unpack('B', f.read(1))[0]
            char = s.unpack('B', f.read(1))[0]
            code.append((offset, length, char))
        message = decode(code)
        for m in message:
            g.write(s.pack('B', m))
        g.close()
    f.close()

def make_parser():
    parser = ArgumentParser(description='LZ77 Encoder/Decoder')
    parser.add_argument('-b',
                        '--binary',
                        action='store_true',
                        help='binary encoding/decoding')
    parser.add_argument('-i',
                        '--interactive',
                        action='store_true',
                        help='interactive encoding/decoding')
    parser.add_argument('-o',
                        '--overflow',
                        action='store_true',
                        help='encode with overflow')
    parser.add_argument('-d',
                        '--decode',
                        nargs='*',
                        metavar='file',
                        help='decode file')
    parser.add_argument('-e',
                        '--encode',
                        nargs='*',
                        metavar='file',
                        help='encode output [files]')
    return parser

################################################################################

if __name__ == '__main__':
    parser = make_parser()
    args = parser.parse_args()
    if args.decode == None and args.encode == None:
        parser.parse_args(['-h'])

    encode_flag = args.encode != None and args.decode == None
    decode_flag = args.decode != None and args.encode == None
    interactive_flag = args.interactive and not args.binary
    not_binary_flag = not args.interactive and not args.binary
    binary_flag = not args.interactive and args.binary
    overflow = args.overflow

    if args.interactive and not args.binary:
        if encode_flag:
            interactive_encode(overflow)
        elif decode_flag:
            interactive_decode()
    elif not_binary_flag:
        if encode_flag:
            if len(args.encode) < 2:
                print('no input file')
                exit(1)
            not_binary_encode(overflow, args.encode[0], args.encode[1:])
        elif decode_flag:
            if len(args.decode) < 1:
                print('no input file')
                exit(1)
            not_binary_decode(args.decode[0])
    elif binary_flag:
        if encode_flag:
            if len(args.encode) < 2:
                print('no input file')
                exit(1)
            binary_encode(overflow, args.encode[0], args.encode[1:])
        elif decode_flag:
            if len(args.decode) < 1:
                print('no input file')
                exit(1)
            binary_decode(args.decode[0])
