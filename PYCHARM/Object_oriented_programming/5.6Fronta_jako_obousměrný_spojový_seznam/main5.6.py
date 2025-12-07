from DoubleLinkedQueue import DoubleLinkedQueue







if __name__ == '__main__':
    my_list = DoubleLinkedQueue()
    my_list.add("Prvek 1")
    my_list.add("Prvek 2")
    my_list.add("Prvek 3")
    my_list.add("Prvek 4")
    my_list.add("Prvek 5")

    for item in my_list:
        print(item)
    print("---")
    for item in reversed(my_list):
        print(item)
    print("---")
    print(my_list.pop())
    print("---")
    for item in my_list:
        print(item)
    print("---")

    print(my_list.count)
    print("---")
    #print(my_list.clear())
    print(my_list.popAll())