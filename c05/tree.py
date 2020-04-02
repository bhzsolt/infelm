# Bodoki-Halmen Zsolt
# bzim1700
# 531/1

class Tree:
    def __init__(self):
        self.data = None
        self.parent = None
        self.left = None
        self.right = None

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
            string += preorder(node.right, tab+1)
            string += preorder(node.left, tab+1) 
            return string
        return preorder(self, 0)

    def depth(self):
        def helper(node):
            if node == None:
                return 0
            return 1 + max(helper(node.left), helper(node.right))
        return helper(self)

    def sibling(self):
        node_data = bfs(self)
        _, d1 = node_data[0]
        node_data[:] = node_data[1:]
        data = [d1]
        for _, d1, d2 in node_data:
            data += [d1, d2]
        return data == sorted(data, reverse=True)

def bfs(node):
    queue = []
    queue.insert(0, (node.depth()-1, node.left, node.right))
    node_data = [(node.depth(), node.data)]
    while len(queue) > 0:
        (depth, nl, nr) = queue.pop()
        if nl.data > nr.data:
            node_data.append((depth, nl.data, nr.data))
        else:
            node_data.append((depth, nr.data, nl.data))

        if (nl.left != None) and (nl.right != None):
            queue.insert(0, (depth-1, nl.left, nl.right))
        if (nr.left != None) and (nr.right != None):
            queue.insert(0, (depth-1, nr.left, nr.right))
    node_data.sort(reverse=True)
    return node_data

def make_tree(string):
    def find(k, par):
        for (x, i) in par:
            if x == k:
                return (x, i)

    if string != '' and '(' not in string and ')' not in string:
        node = Tree()
        node.data = int(string.strip())
        return node
    par = []
    stack = []
    k = 0
    for i in range(len(string)):
        if string[i] == '(':
            stack.append(k)
            par.append((k, i))
            k += 1
        elif string[i] == ')':
            l = stack.pop()
            par.append((l, i))
    node = Tree()
    node.data = int(string.split(' ')[0])
    (k, l0) = par[0]
    (_, l1) = find(k, par[1:])
    node.left = make_tree(string[l0+1:l1])
    node.left.parent = node
    (k, r1) = par.pop()
    (_, r0) = find(k, par)
    node.right = make_tree(string[r0+1:r1])
    node.right.parent = node
    return node
