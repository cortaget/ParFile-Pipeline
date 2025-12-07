from DoubleLinkedQueue import DoubleLinkedQueue







if __name__ == '__main__':
    my_list = DoubleLinkedQueue()
    my_list.add("Prvek 1")
    my_list.add("Prvek 2")
    my_list.add("Prvek 3")
    my_list.add("Prvek 4")
    my_list.add("Prvek 5")

    print("Prvek 1" in my_list)
    if "Prvek 1" in my_list:
        print("Prvek 1 je v DoubleLinkedQueue")