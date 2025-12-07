


class Zivnostnik:
    """ Trida reprezentuje zivnostnika """

    @staticmethod
    def factory_from_obchodni_nazev(obchodni_nazev : str):
        """
        Staticka metoda vytvorit zivnostnika z obchodniho nazvu

        :param obchodni_nazev: Napriklad Jan Novak
        :return: Novy objekt tridy Zinvostnik
        """
        data = obchodni_nazev.split(' ')

        if(len(data) !=  2):
            raise Exception("Nelze parsovat obchodni nazev")

        return Zivnostnik(data[0], data[1])

    def __init__(self, jmeno : str, prijmeni : str):
        """
        Konstruktor nastavi jmeno a prijimeni
        :param jmeno: Jmeno zivnostnika
        :param prijmeni: Prijimeni zivnostnika
        """
        if(len(jmeno) < 1 or len(prijmeni) < 0):
            raise Exception("Jmeno a prijimani musi byt definovnao")

        self.jmeno = jmeno
        self.prijmeni = prijmeni


pepa = Zivnostnik.factory_from_obchodni_nazev("Josef Novák")
print(pepa.prijmeni)





class Firma:
    """ Třída reprezentuje firmu"""

    def __init__(self, nazev, pravni_forma):
        """
        Vytvoří instanci firmy
        :param nazev: Název například Maso a uzeniny od Pavlíka
        :param pravni_forma: Právní forma, například s.r.o, nebo a.s. apod.
        """
        self.jmeno = nazev
        self.pravni_forma = pravni_forma


    @staticmethod
    def factory_from_obchodni_nazev(obchodni_nazev : str):
        """
        Statická metoda vytvoří firmu z obchodního názvu

        :param obchodni_nazev: Například Maso a uzeniny od Pavlíka, s.r.o.
        :return: Nový objekt třídy Firma
        """
        data = obchodni_nazev.rsplit(',', 1)

        if(len(data) !=  2):
            raise Exception("Nelze parsovat obchodni nazev")

        nazev = data[0].strip()
        pravni_forma = data[1].strip()

        if(len(nazev) < 1 or len(pravni_forma) < 1):
            raise Exception("Nelze parsovat obchodni nazev")

        return Firma(nazev, pravni_forma)


sporka = Firma.factory_from_obchodni_nazev("Česká spořitelna, a.s.")
print(sporka.pravni_forma) #ma vypsat "a.s."

