class Zbozi:
    def __init__(self):
        self._vaha = 0

    @property
    def vaha(self):
        return self._vaha

    @vaha.setter
    def vaha(self,x):
        if(x < 0):
            raise Exception("Zaporna vaha nesmi existovat")

        self._vaha = x

rohlik = Zbozi()
rohlik.vaha = 10;
print(rohlik.vaha)

#rohlik.vaha = -20; #toto vyhodi vyjimku
print("---")

class Obdelnik:
    def __init__(self, a, b):
        self._a = 0
        self._b = 0
        self.a = a
        self.b = b

    @property
    def a(self):
        return self._a

    @a.setter
    def a(self, hodnota):
        if hodnota < 0:
            raise Exception("Strana a nemůže být záporná.")
        self._a = hodnota

    @property
    def b(self):
        return self._b

    @b.setter
    def b(self, hodnota):
        if hodnota < 0:
            raise Exception("Strana b nemůže být záporná.")
        self._b = hodnota

    def obvod(self):
        return 2 * (self._a + self._b)

    def obsah(self):
        return self._a * self._b


# --- Test ---
o = Obdelnik(5, 3)
print("Obvod:", o.obvod())
print("Obsah:", o.obsah())

o.a = 10  # OK
print("Nová strana a:", o.a)

#o.b = -2  # Vyvolá výjimku