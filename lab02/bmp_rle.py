#!/bin/python3
# Bodoki-Halmen Zsolt
# bzim1700
# 531/1

import struct
from sys import argv
from os import path
from functools import reduce

#print('Type:', bmp.read(2).decode()) [0:2]
#print('Size: %s' % struct.unpack('I', bmp.read(4))) [2:6]
#print('Reserved 1: %s' % struct.unpack('H', bmp.read(2))) [6:8]
#print('Reserved 2: %s' % struct.unpack('H', bmp.read(2))) [8:10]
#print('Offset: %s' % struct.unpack('I', bmp.read(4))) [10:14]

#print('DIB Header Size: %s' % struct.unpack('I', bmp.read(4))) [14:18]
#print('Width: %s' % struct.unpack('I', bmp.read(4))) [18:22]
#print('Height: %s' % struct.unpack('I', bmp.read(4))) [22:26]
#print('Colour Planes: %s' % struct.unpack('H', bmp.read(2))) [26:28]
#print('Bits per Pixel: %s' % struct.unpack('H', bmp.read(2))) [28:30]
#print('Compression Method: %s' % struct.unpack('I', bmp.read(4))) [30:34]
#print('Raw Image Size: %s' % struct.unpack('I', bmp.read(4))) [34:38]
#print('Horizontal Resolution: %s' % struct.unpack('I', bmp.read(4))) [38:42]
#print('Vertical Resolution: %s' % struct.unpack('I', bmp.read(4))) [42:46]
#print('Number of Colours: %s' % struct.unpack('I', bmp.read(4))) [46:50]

def rle_encode(decoded, encoded):
    with open(decoded, 'rb') as bmp:
        header = bmp.read(54)
        raw = bmp.read()
        print(type(raw))

    flat = []
    p = b'0'
    first = True
    c = 0
    for x in raw:
        if x != p:
            if not first:
                flat.append((p, c))
            c = 1
        else:
            c += 1
        p = x
        first = False
    flat.append((x, c))

    with open(encoded, 'wb') as f:
        f.write(header)
        f.write(struct.pack('I', len(flat)))
        for x, c in flat:
            f.write(struct.pack('B', x))
            f.write(struct.pack('H', c))

def rle_decode(encoded, decoded):
    with open(encoded, 'rb') as f:
        header = f.read(54)
        length = struct.unpack('I', f.read(4))[0]
        flat = []
        for i in range(length):
            x = f.read(1)
            c = struct.unpack('H', f.read(2))[0]
            flat.append((x,c))
    real = []
    for x, c in flat:
        for i in range(c):
            real.append(x)

    with open(decoded, 'wb') as bmp:
        bmp.write(header)
        for x in real:
            bmp.write(x)

AND = lambda x,y: x and y
check_extension = lambda x: path.splitext(x)[1].lower() == '.bmp'

################################################################################

if (len(argv) < 2 
        or not reduce(AND, map(path.isfile, argv[1:]))
        or not reduce(AND, map(check_extension, argv[1:]))):
    print('usage: {} [file.bmp]'.format(argv[0]))
    exit(1)

images = argv[1:]

for image in images:
    rle_encode(image, image+'.bh')
    rle_decode(image+'.bh', image+'.bh.bmp')
