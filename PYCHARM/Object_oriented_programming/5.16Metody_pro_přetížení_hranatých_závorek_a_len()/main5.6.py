from DoubleLinkedQueue import DoubleLinkedQueue







if __name__ == '__main__':
    my_list = DoubleLinkedQueue()
    my_list.add("Prvek 1")
    my_list.add("Prvek 2")
    my_list.add("Prvek 3")
    my_list.add("Prvek 4")
    my_list.add("Prvek 5")

    print("Pocet prvku v DoubleLinkedQueue:", len(my_list))
    print(my_list[0])  # Vytiskne "Prvek 1"
    my_list[2]="5"  # Vytiskne "Prvek 3"
    print(my_list[2])  # Vytiskne "Prvek 2"