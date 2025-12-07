import re
class Zbozi:
    """ Trida zbozi pro ukazu prikladu relacnich operatoru"""

    def __init__(self, nazev: str, vaha: float):
        """
        Pri vytvoreni se nastavuje nazev zbozi a jeho vaha
        :param nazev: Nazev musi byt znaky v rozsahu 1 az 200 znaku
        :param vaha: Vaha musi byt kladne a nenulove cislo
        """
        if not re.match(r"^[\D ]{1,200}$", nazev):
            raise Exception('Nazev musi byt v rozsahu 1 az 200 znaku')
        if vaha <= 0:
            raise Exception('Vaha nesmi byt zapojna')

        self._nazev = nazev
        self._vaha = vaha

    def __lt__(self, other):
        """
        Metoda zjistuje jestli je zbozi mensi nez druhe zbozi. Porovnava se pouze vaha.
        :param other: Trida pro porovnani, musi to byt instance Zbozi
        :return: True pokud je self mensi nez other
        """
        if (not isinstance(other, Zbozi)):
            raise Exception('Porovnavat lze jen zbozi mezi sebou')

        return self._vaha < other._vaha

    def __gt__(self, other):
        """
        Metoda zjistuje jestli je zbozi vetsi nez druhe zbozi. Porovnava se pouze vaha.
        :param other: Trida pro porovnani, musi to byt instance Zbozi
        :return: True pokud je self vetsi nez other
        """
        if (not isinstance(other, Zbozi)):
            raise Exception('Porovnavat lze jen zbozi mezi sebou')

        return self._vaha > other._vaha

    def __le__(self, other):
        """
        Metoda zjistuje jestli je zbozi mensi nebo rovno druhe zbozi. Porovnava se pouze vaha.
        :param other: Trida pro porovnani, musi to byt instance Zbozi
        :return: True pokud je self mensi nebo rovno other
        """
        if (not isinstance(other, Zbozi)):
            raise Exception('Porovnavat lze jen zbozi mezi sebou')

        return self._vaha <= other._vaha

    def __ge__(self, other):
        """
        Metoda zjistuje jestli je zbozi vetsi nebo rovno druhe zbozi. Porovnava se pouze vaha.
        :param other: Trida pro porovnani, musi to byt instance Zbozi
        :return: True pokud je self vetsi nebo rovno other
        """
        if (not isinstance(other, Zbozi)):
            raise Exception('Porovnavat lze jen zbozi mezi sebou')

        return self._vaha >= other._vaha


    def __eq__(self, other):
        """
        Metoda zjistuje jestli je zbozi rovno druhe zbozi. Porovnava se pouze vaha.
        :param other: Trida pro porovnani, musi to byt instance Zbozi
        :return: True pokud je self rovno other
        """
        if (not isinstance(other, Zbozi)):
            raise Exception('Porovnavat lze jen zbozi mezi sebou')

        return self._vaha == other._vaha

    def __ne__(self, other):
        """
        Metoda zjistuje jestli je zbozi nerovno druhe zbozi. Porovnava se pouze vaha.
        :param other: Trida pro porovnani, musi to byt instance Zbozi
        :return: True pokud je self nerovno other
        """
        if (not isinstance(other, Zbozi)):
            raise Exception('Porovnavat lze jen zbozi mezi sebou')

        return self._vaha != other._vaha


    def __hash__(self):
        """
        Metoda vraci hash hodnotu pro instanci tridy Zbozi
        :return: Hash hodnotu jako cele cislo
        """
        return hash((self._nazev, self._vaha))






kilo_brambor = Zbozi("Bramobra", 1)
krabice_mleka = Zbozi("Mleko", 1.029)
if(kilo_brambor < krabice_mleka):
    print("Svet je jeste v poradku")


print(kilo_brambor > krabice_mleka)   # False
print(kilo_brambor <= krabice_mleka)  # True
print(kilo_brambor >= krabice_mleka)  # False
print(kilo_brambor == krabice_mleka)  # False
print(kilo_brambor != krabice_mleka)  # True


zbozi1 = Zbozi("Mrkev", 1)
print(hash(zbozi1))


zbozi1 = Zbozi("Mrkev", 1)
zbozi2 = Zbozi("Mrkev", 1)
zbozi3 = Zbozi("Celer", 1)

x = set()
x.add(zbozi1)
x.add(zbozi2)
x.add(zbozi3)
print(len(x))