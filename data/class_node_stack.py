class EmptyStackException(Exception):
    pass


class Node():
    """"Класс узла"""

    def __init__(self, element=None, next_node=None):
        self.data = element
        self.next_node = next_node

    def __str__(self):
        return self.data

    def __repr__(self):
        return self.__str__()


class Stack():
    """"Класс СТЭКА"""

    def __init__(self):
        self.top = None
        self.size = 0

    def push(self, data):
        self.top = Node(data, self.top)
        self.size += 1

    def pop(self):
        if self.top:
            val = self.top.data
            self.top = self.top.next_node
            self.size -= 1
            return val
        else:
            raise EmptyStackException
