from DoubleLinkedQueue import DoubleLinkedQueue







if __name__ == '__main__':

    parta = ["Karel", "Petra", "Mirka"]
    iterator_party = iter(parta)
    try:
        print(next(iterator_party))
        print(next(iterator_party))
        print(next(iterator_party))
        print(next(iterator_party))  # Tohle vyhodi vyjimku StopIteration error protoze dalsi uz nema
    except(StopIteration):
        pass

    print("----")
    for jmeno in parta:
        print(jmeno)