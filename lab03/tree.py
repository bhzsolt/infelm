# Bodoki-Halmen Zsolt
# bzim1700
# 531/1

from priority_queue import PriorityQueue

class Tree:
    root = None
    current_node = None
    code = ''
    label = ''
    i = 0
    def __init__(self):
        self.data = None
        self.frequency = None
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
            string += str(node.data) + ':' + str(node.frequency) + '\n'
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
        def bfs(node):
            queue = []
            queue.insert(0, (node.depth()-1, node.left, node.right))
            node_data = [(node.depth(), node.frequency)]
            while len(queue) > 0:
                (depth, nl, nr) = queue.pop()
                if nl.frequency > nr.frequency:
                    node_data.append((depth, nl.frequency, nr.frequency))
                else:
                    node_data.append((depth, nr.frequency, nl.frequency))
            
                if (nl.left != None) and (nl.right != None):
                    queue.insert(0, (depth-1, nl.left, nl.right))
                if (nr.left != None) and (nr.right != None):
                    queue.insert(0, (depth-1, nr.left, nr.right))
            node_data.sort(reverse=True)
            return node_data

        node_data = bfs(self)
        _, d1 = node_data[0]
        node_data[:] = node_data[1:]
        data = [d1]
        for _, d1, d2 in node_data:
            data += [d1, d2]
        return data == sorted(data, reverse=True)
    
    def update_data(self):
        def data_to_list(data):
            if isinstance(data, tuple):
                tmp_1 = [data[0]]
                if isinstance(data[0], list):
                    tmp_1 = data[0]
                tmp_2 = [data[1]]
                if isinstance(data[1], list):
                    tmp_2 = data[1]
                return tmp_1 + tmp_2
            else:
                return [data]
        self.data = (data_to_list(self.left.data), data_to_list(self.right.data))
    
    def update_data_recursively(self):
        node = self.parent
        while node != None:
            node.update_data()
            node = node.parent
    
    def find_node(self, elem):
        code = ''
        node = self
        while node.data != elem:
            if elem in node.data[0]:
                code += '0'
                node = node.left
            elif elem in node.data[1]:
                code += '1'
                node = node.right
            else:
                return None, ''
        return node, code

    def find_frequency(self, frequency, depth):
        queue = []
        queue.insert(0, (1, self.left))
        queue.insert(0, (1, self.right))
        node_data = [(0, self.frequency)]
        while len(queue) > 0:
            (d, node) = queue.pop()
            if d >= depth:
                break
            if node.frequency == frequency:
                return node
            if (node.left != None) and (node.right != None):
                queue.insert(0, (d+1, node.left))
                queue.insert(0, (d+1, node.right))
    
    def swap(x, y):
        if x.parent.left == x:
            if y.parent.left == y:
                x.parent.left, y.parent.left = y, x
            else:
                x.parent.left, y.parent.right = y, x
        else:
            if y.parent.left == y:
                x.parent.right, y.parent.left = y, x
            else:
                x.parent.right, y.parent.right = y, x
        x.parent, y.parent = y.parent, x.parent
        x.update_data_recursively()
        y.update_data_recursively()

    def encode_character(self, m):
        x, code = self.find_node(m)
        while x != None:
            y = self.find_frequency(x.frequency, len(code))
            if y != None:
                Tree.swap(x, y)
                x.frequency += 1
                x = x.parent
            else:
                x.frequency += 1
                x = x.parent
        return code

    def decode(self, code):
        message = []
        self.code += code
        while self.i < len(self.code):
            c = self.code[self.i]
            if c == '0':
                self.current_node = self.current_node.left
                self.label += '0'
            elif c == '1':
                self.current_node = self.current_node.right
                self.label += '1'
            if not isinstance(self.current_node.data, tuple):
                message.append(self.current_node.data)
                x = self.current_node
                while x != None:
                    y = self.find_frequency(x.frequency, len(self.label))
                    if y != None:
                        Tree.swap(x, y)
                        x.frequency += 1
                        x = x.parent
                    else:
                        x.frequency += 1
                        x = x.parent
                self.label = ''
                self.current_node = self.root
            self.i += 1
        return message

def make_tree(data):
    queue = PriorityQueue()
    for d in data:
        node = Tree()
        node.data = d
        node.frequency = 1
        queue.push(node)
     
    while queue.size() > 1:
        node = Tree()
        node.left = queue.pop()
        node.left.parent = node
        node.right = queue.pop()
        node.right.parent = node
        node.frequency = node.left.frequency + node.right.frequency
        node.update_data()
        queue.push(node)
    
    root = queue.pop()
    root.root = root
    root.current_node = root
    return root
