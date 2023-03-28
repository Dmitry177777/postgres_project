class Node():
    """"Класс узла"""

    def __init__(self, data=None, next=None):
        self.data = data
        self.next = None

    def __str__(self):
        if self.data:
            return self.data.__str__()
        else:
            return 'Empty Node'

    def __repr__(self):
        return self.__str__()


class LinkedList():
    "дносвязный список"

    head = None

    def __init__(self):
        self.head = None

    def insert_beginning(self, newdata):
        "добавление в начало списка"
        NewNode = Node(newdata)
        NewNode.next = self.head
        self.head = NewNode

    def insert_at_end(self, newdata):
        "добавление в конец списка"
        NewNode = Node(newdata)
        if self.head is None:
            self.head = NewNode
            return
        laste = self.head
        while (laste.next):
            laste = laste.next
        laste.next = NewNode

    def to_list(self):
        """ возврат данные односвязного списка"""
        ll_list = []
        node = self.head
        if node is None:
            return ll_list
        while node:
            # print(node)
            ll_list.append(node)
            node = node.next

        return ll_list

    def get_data_by_id(self, id):
        """возврат данных по ключу id"""

        node = self.head
        ll_id = {}
        try:
            while node:

                # print(node.data['id'])
                if node.data['id'] == id:
                    ll_id = node
                    break
                node = node.next

        except(TypeError):
            print('Данные не являются словарем или в словаре нет id')
            return ""
        return ll_id

    def print_ll(self):
        ll_string = ''
        node = self.head
        if node is None:
            print(None)
        while node:
            ll_string += f' {str(node.data)} ->'
            node = node.next

        ll_string += ' None'
        print(ll_string)
        return ll_string
