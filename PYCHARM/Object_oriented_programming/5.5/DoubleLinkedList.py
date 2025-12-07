from Node import Node

class DoubleLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None


    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            self.tail = new_node
            return
        self.tail.next = new_node
        new_node.prev = self.tail
        self.tail = new_node


    def __iter__(self):
        self.current = self.head
        return self

    def __next__(self):
        if not self.current:
            raise StopIteration
        value = self.current.data
        self.current = self.current.next
        return value

    def __reversed__(self):
        self.current = self.tail
        while self.current:
            yield self.current.data
            self.current = self.current.prev