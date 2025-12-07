def prepinac_svetla():
    je_svetlo = False

    def prepni():
        nonlocal je_svetlo
        je_svetlo = not je_svetlo
        return je_svetlo

    return prepni


prepinac1 = prepinac_svetla();
print(prepinac1())
print(prepinac1())
print(prepinac1())
print(prepinac1())





def vytvor_pocitadlo_navstevniku():
    pocet_navstevniku = 0
    def pridej_navstevnika():
        nonlocal pocet_navstevniku
        pocet_navstevniku += 1
        return pocet_navstevniku
    return pridej_navstevnika



pridej_navstevnika = vytvor_pocitadlo_navstevniku()
pocet = pridej_navstevnika()
print(pocet)
pocet = pridej_navstevnika()
print(pocet)
pocet = pridej_navstevnika()
print(pocet)