#!/bin/python3

import struct
from functools import reduce
from sys import argv

def add(list_, current):
    index = len(list_)-1
    if list_ != []:
        previous, count = list_[index]
        if previous == current:
            list_[index] = (current, count+1)
        else:
            list_.append((current, 1))
    else:
        list_.append((current, 1))

image = argv[1]



with open(image, 'rb') as bmp:
    data = bmp.read()

    offset = struct.unpack('I', data[10:14])[0]
    w = struct.unpack('I', data[18:22])[0]
    h = struct.unpack('I', data[22:26])[0]
    bpp = struct.unpack('H', data[28:30])[0]
    print('w * h =', w, '*', h, '=', w*h)
    print('w * h * 3 =', w*h*3)
    print(len(data[offset:]))
    print('Bits per pixel:', bpp)

    red = []
    blue = []
    green = []
    for x in range(w*h):
        r, g, b = struct.unpack('BBB', data[offset+x*3:offset+x*3+3])
        add(red, r)
        add(blue, b)
        add(green, g)
    
    print(len(red), len(blue), len(green), len(red)+len(green)+len(blue))
    print(max(map(lambda x: x[1], red)))
    print(max(map(lambda x: x[1], green)))
    print(max(map(lambda x: x[1], blue)))
