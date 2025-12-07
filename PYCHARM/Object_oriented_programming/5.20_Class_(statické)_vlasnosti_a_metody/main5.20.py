class KonfiguraceKonference:

    _maximalni_pocet_ucastniku = 0

    @classmethod
    def set_maximalni_pocet_ucastniku(cls, max):
        cls._maximalni_pocet_ucastniku = max;

    @classmethod
    def get_maximalni_pocet_ucastniku(cls):
        return cls._maximalni_pocet_ucastniku;

    def __new__(cls, *args, **kwargs):
        raise Exception("Nelze vytvorit instanci tridy KonfiguraceKonference, pouzijte staticke metody")


print(KonfiguraceKonference.get_maximalni_pocet_ucastniku())

KonfiguraceKonference.set_maximalni_pocet_ucastniku(212)
print(KonfiguraceKonference.get_maximalni_pocet_ucastniku())






#mojeKonfigurace = KonfiguraceKonference()
#mojeKonfigurace.set_maximalni_pocet_ucastniku(300)
#print(mojeKonfigurace.get_maximalni_pocet_ucastniku())