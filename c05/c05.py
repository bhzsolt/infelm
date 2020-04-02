#!/bin/python3
# Bodoki-Halmen Zsolt
# bzim1700
# 531/1

from sys import argv
import tree as t

def help(exitcode):
    print('usage: {} input'.format(argv[0]))
    print('\tinput:\ta tree in the format: value (left) (right)')
    print('\t\twhere left and right have the same format, omitting empty parantheses')
    exit(exitcode)


################################################################################

if __name__ == '__main__':
    if len(argv) < 2:
        help(1)
    
    with open(argv[1], 'r') as f:
        contents = f.read().strip()
    root = t.make_tree(contents)

    print(root.sibling())
    #print(root)
    #print(root.depth())
    #node = root.left.right
    #print(node.parent)

