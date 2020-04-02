# Bodoki-Halmen Zsolt
# bzim1700
# 531/1

from priority_queue import PriorityQueue

class Tree:
    def __init__(self, data=None, leafs=None, huffman_data=None, shannon_fano_data=None):
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
        
        self.left = None
        self.right = None
        self.prob = 0.0
        self.data = None

        if huffman_data == None and shannon_fano_data == None:
            if data != None:
                self.prob = data[0]
                self.data = data[1]
            if leafs != None:
                self.left = leafs[0]
                self.right = leafs[1]
                self.prob = leafs[0].prob + leafs[1].prob
                self.data = (data_to_list(leafs[0].data), data_to_list(leafs[1].data))
        elif shannon_fano_data == None:
            self.huffmanFromList(huffman_data)
        else:
            shannon_fano_data.sort(reverse=True)
            root = self.shannonFanoFromList(shannon_fano_data)
            self.left = root.left
            self.right = root.right
            self.prob = root.prob
            self.data = root.data

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
            string += preorder(node.left, tab+1) 
            string += preorder(node.right, tab+1)
            return string
        return preorder(self, 0)

    def huffmanFromList(self, huffman_data):
        queue = PriorityQueue()
        for x in huffman_data:
            queue.push(Tree(x))

        while queue.size() > 1:
            t0 = queue.pop()
            t1 = queue.pop()
            t2 = Tree(leafs=(t0, t1))
            queue.push(t2)
        
        root = queue.pop()

        self.left = root.left
        self.right = root.right
        self.prob = root.prob
        self.data = root.data

    def shannonFanoFromList(self, shannon_fano_data):
        def partition(x):
            # x = [(p, e)]
            return [(x[:i], x[i:]) for i in range(1, len(x))]

        def find_best(x):
            #x = [(x0, x1)]
            def keyfunc(x):
                x0, x1 = x
                x0s = 0.0
                for (p,e) in x0:
                    x0s += p
                x1s = 0.0
                for (p, e) in x1:
                    x1s += p
                return abs(x0s - x1s)
            return min(x, key=keyfunc)

        if len(shannon_fano_data) == 1:
            return Tree(data=shannon_fano_data[0])  
        
        xl, xr = find_best(partition(shannon_fano_data))
        left = self.shannonFanoFromList(xl)
        right = self.shannonFanoFromList(xr)
        return Tree(leafs=(left, right))

    def findBinaryCode(self, elem):
        code = None
        node = None
        if elem in self.data[0]:
            code = 0
            node = self.left
        else:
            code = 1
            node = self.right

        while node.data != elem:
            if elem in node.data[0]:
                code *= 2
                node = node.left
            else:
                code *= 2
                code += 1
                node = node.right
        return code

    def findStringCode(self, elem):
        code = ''
        node = None
        if elem in self.data[0]:
            code = '0'
            node = self.left
        else:
            code = '1'
            node = self.right

        while node.data != elem:
            if elem in node.data[0]:
                code += '0'
                node = node.left
            else:
                code += '1'
                node = node.right
        return code
