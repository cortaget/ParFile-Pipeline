from DoubleLinkedList import DoubleLinkedList







if __name__ == '__main__':
    my_list = DoubleLinkedList()
    my_list.append("Prvek 1")
    my_list.append("Prvek 2")
    my_list.append("Prvek 3")
    my_list.append("Prvek 4")
    my_list.append("Prvek 5")

    for item in my_list:
        print(item)
    print("---")
    for item in reversed(my_list):
        print(item)
