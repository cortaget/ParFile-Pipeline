from Node import Node

class DoubleLinkedQueue:
    def __init__(self):
        self.head = None
        self.tail = None
        self.count = 0


    def add(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            self.tail = new_node
            return
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
        self.count += 1

    def pop(self):
        if not self.head:
            raise IndexError("pop from empty DoubleLinkedQueue")
        data = self.head.data
        self.head = self.head.next
        if self.head:
            self.head.prev = None
        else:
            self.tail = None
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

    def __len__(self):
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


    def __getitem__(self, item):
        if item < 0 or item >= self.count:
            raise IndexError("Index out of range")
        current = self.head
        for _ in range(item):
            current = current.next
        return current.data


    def __setitem__(self, key, value):
        if key < 0 or key >= self.count:
            raise IndexError("Index out of range")
        current = self.head
        for _ in range(key):
            current = current.next
        current.data = value


    def __contains__(self, item):
        current = self.head
        while current:
            if current.data == item:
                return True
            current = current.next
        return False

