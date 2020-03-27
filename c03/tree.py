# Bodoki-Halmen Zsolt
# bzim1700
# 531/1

from priority_queue import PriorityQueue

class Tree:
    def __init__(self, data=None, symbols=None, children=None):
        def to_list(data):
            if isinstance(data, tuple):
                tmp = []
                for e in data:
                    if isinstance(e, list):
                        for l in e:
                            tmp.append(l)
                    else:
                        tmp.append(e)
                return tmp
            else:
                return [data]
            
        if children == None:
            if data != None:
                self.data = data[1]
                self.prob = data[0]
            else:
                self.data = None
                self.prob = None
            self.children = []
            self.symbol = None
        else:
            self.data = tuple([to_list(x.data) for x in children])
            self.prob = 0.0
            i = 0
            for c in children:
                self.prob += c.prob
                c.symbol = symbols[i]
                i += 1
            self.children = children
            self.symbol = None
    
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
            for c in node.children:
                string += preorder(c, tab+1)
            return string
        return preorder(self, 0)
    
    def findCode(self, elem):
        def findCode(node, elem, string):
            if node.data == elem:
                return string + node.symbol
            if len(node.children) == 0:
                return None
            
            for i in range(len(node.children)):
                tmp = findCode(node.children[i], elem, string + node.symbol)
                if tmp != None:
                    return tmp
        return findCode(self, elem, '')

def make_tree(symbols, data):
    s = len(symbols)
    n = len(data)
    k = (n - 2) % (s - 1) + 2
    queue = PriorityQueue()
    for i in range(n):
        queue.push(Tree(data[i]))

    leafs = []
    for i in range(k):
        leafs.append(queue.pop())
    queue.push(Tree(symbols=symbols, children=leafs))
    
    while queue.size() > 1:
        leafs = []
        for i in range(s):
            leafs.append(queue.pop())
        queue.push(Tree(symbols=symbols, children=leafs))
    
    root = queue.pop()
    root.symbol = ''
    return root
