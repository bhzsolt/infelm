#!/bin/python3
# Bodoki-Halmen Zsolt
# bzim1700
# 531/1

import struct
from sys import argv
from os import listdir
from os import path
from os import mkdir

def add(list_, current):
    index = len(list_)-1
    previous, count = -1, -1
    if list_ != []:
        previous, count = list_[index]
    if previous == current:
        list_[index] = (current, count+1)
    else:
        list_.append((current, 1))

def create_runs(data, w, h):
    red = []
    green = []
    blue = []
    for x in range(w*h):
        r, g, b = struct.unpack('BBB', data[x*3:x*3+3])
        add(red, r)
        add(green, g)
        add(blue, b)
    return red, green, blue

def write_color(fp, color):
    fp.write(struct.pack('I', len(color)))
    for value, count in color:
        fp.write(struct.pack('HH', value, count))

def read_color(data):
    length = struct.unpack('I', data[0:4])[0]
    print(length)
    color = []
    for r in range(length):
        value, count = struct.unpack('HH', data[(r*4+4):(r*4+8)])
        for x in range(count):
            color.append(value)
    return color, 4+4*length

def encode(input_file, output_file=None):
    if output_file == None:
        output_file = input_file+'.bh'
    
    with open(input_file, 'rb') as bmp:
        data = bmp.read()

    offset = struct.unpack('I', data[10:14])[0]
    w = struct.unpack('I', data[18:22])[0]
    h = struct.unpack('I', data[22:26])[0]

    header = data[:offset]
    r,g,b = create_runs(data[offset:], w, h)
    print('rgb:', len(r), len(g), len(b))

    with open(output_file, 'wb') as f:
        f.write(header)
        write_color(f, r)
        write_color(f, g)
        write_color(f, b)

def decode(input_file, output_file=None):
    if output_file == None:
        output_file = input_file+'.bmp'

    with open(input_file, 'rb') as f:
        data = f.read()

    offset = struct.unpack('I', data[10:14])[0]
    w = struct.unpack('I', data[18:22])[0]
    h = struct.unpack('I', data[22:26])[0]

    header = data[:offset]
    r, add = read_color(data[offset:])
    offset += add
    g, add = read_color(data[offset:])
    offset += add
    b, add = read_color(data[offset:])

    with open(output_file, 'wb') as bmp:
        bmp.write(header)
        for i in range(w*h):
            bmp.write(struct.pack('BBB', r[i], g[i], b[i]))

################################################################################

if __name__ == '__main__':
    if len(argv) == 1:
        images = listdir('input')
    else:
        images = argv[1:]

    if not path.isdir('output'):
        mkdir('output')

    for image in images:
        input_file = 'input/' + image
        output_file_bh = 'output/' + image + '.bh'
        output_file_bmp = 'output/' + image
        if not path.isfile(input_file):
            print('{} not a valid bmp file'.format(input_file))
            continue
        encode(input_file, output_file_bh)
        decode(output_file_bh, output_file_bmp)
