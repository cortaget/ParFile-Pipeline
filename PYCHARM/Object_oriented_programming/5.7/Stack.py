from Node import Node

class Stack:
    def __init__(self):
        self.head = None
        self.count = 0


    def add(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        else:
            new_node.next = self.head
            self.head = new_node
        self.count += 1




    def pop(self):
        if not self.head:
            raise IndexError("Pop z prázdného zásobníku")

        data = self.head.data
        self.head = self.head.next
        self.count -= 1
        return data

    def popAll(self):
        if not self.head:
            raise IndexError("popAll from empty DoubleLinkedQueue")
        data =[]
        while self.head:
            data.append(self.pop())

        return data


    def count(self):
        return self.count

    def clear(self):
        self.head = None
        self.tail = None
        self.count = 0




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