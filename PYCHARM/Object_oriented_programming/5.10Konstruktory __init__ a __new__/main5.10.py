class Zbozi:
    def __new__(cls, nazev, cena):
        if not isinstance(cena,(int,float)) or cena < 0 or not nazev:
            instance = None
        else:
            instance = super().__new__(cls)

        return instance

    def __init__(self, nazev, cena):
        self.nazev = nazev
        self.cena = cena


a = Zbozi("Rohlik", 5)
b = Zbozi("Hackers item", -10)
c = Zbozi("", 10)
d = Zbozi("Chleba", "stovka")
print(a)
print(b)
print(c)
print(d)