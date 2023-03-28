
class Node():
    """"Класс узла"""

    def __init__(self, element=None, next_node=None):
        self.data = element
        self.next_node = next_node


    def __str__(self):
        if self.data:
            return self.data.__str__()
        else:
            return 'Empty Node'

    def __repr__(self):
        return self.__str__()


class Queue(object):
    "Цепная очередь"

    def __init__(self):
        self.head = Node()
        self.tail = Node()
        self.length = 0

    def get_length(self):
        "Получи длину"
        return self.length

    def is_empty(self):
        "Судите, пусто ли оно"
        if self.length == 0:
            return True
        return False

    def enqueue(self, elem):
        "Операция входа"

        tmp = Node(elem)
        if self.is_empty():
            self.head = tmp
            self.tail = tmp
        else:
            self.tail.next_node = tmp
            self.tail = tmp
        self.length += 1

    def dequeue(self):
        "Операция Dequeue"
        if self.is_empty():
            return None
        else:
            del_elem = self.head.data
            self.head = self.head.next_node
            self.length -= 1
            return del_elem

    # def show_queue(self):
    #     "Показать очередь"
    #     if self.is_empty():
    #         raise ValueError("LKQueue is empty!")
    #
    #     j = self.length
    #     tmp = self.head
    #     while j > 0:
    #         print(tmp.data)
    #         tmp = tmp.next
    #         j -= 1
