# Bodoki-Halmen Zsolt
# bzim1700
# 531/1

class PriorityQueue:
    def __init__(self):
        self.queue = []

    def push(self, leaf):
        if len(self.queue) == 0:
            self.queue.append(leaf)
            return
        index = 0
        while index < len(self.queue) and self.queue[index].prob < leaf.prob:
            index += 1
        if index == len(self.queue):
            self.queue.append(leaf)
            return
        self.queue.insert(index, leaf)

    def pop(self):
        if len(self.queue) == 0:
            return None
        tmp = self.queue[0]
        self.queue[:] = self.queue[1:]
        return tmp

    def empty(self):
        return len(self.queue) == 0

    def size(self):
        return len(self.queue)
