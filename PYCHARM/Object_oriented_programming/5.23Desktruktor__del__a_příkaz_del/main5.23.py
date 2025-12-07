x = "Ahoj"
print(x)
del x
#print(x)

ovoce = ["banan", "jahoda", "brambor", "jablko"]
del ovoce[2]
print(ovoce)
print("---")


class Zbozi:

    def __init__(self,nazev):
        self.nazev = nazev

    def __del__(self):
        print("Zbozi "+str(self.nazev)+" bylo vymazano z pameti")


z = Zbozi("Rohlik")
del z
#Objekt se smazal okamžitě, protože po del z už na něj neexistuje žádná reference.

print()
z = Zbozi("Rohlik")
print("Konec programu")#Python na konci programu uvolní všechny proměnné, takže objekt z je zničen při ukončení běhu.


z = Zbozi("Rohlik")
me_oblibene_zbozi = z

del z
print("Po smazání z")
print("Konec programu")

#Proměnná z byla smazána, ale me_oblibene_zbozi stále odkazuje na stejný objekt. Objekt se smaže až když zmizí všechny reference (tedy i me_oblibene_zbozi).