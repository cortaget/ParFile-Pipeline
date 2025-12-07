from Auto import Auto







if __name__ == '__main__':
    car = Auto(30, 12.5)
    print("Aktualni stav nadrze:", car.aktualni_stav_nadrze())
    car.natankuj(22.5)
    print("Aktualni stav nadrze:", car.aktualni_stav_nadrze())
    car.popojed(20)
    print("Aktualni stav nadrze:", car.aktualni_stav_nadrze())
    print("Najeto km:", car.aktualni_stav_najetych_km())


    """
    1
            objem_nadrze_l, spotreba_na_100_km_l, aktualni_objem_paliva_v_nadrzi_l
            
    2
            public: objem_nadrze_l, spotreba_na_100_km_l
            private: _aktualni_objem_paliva_v_nadrzi_l (_ poze rada nepouzivat to jako public)
            
    3       
            __init__ - kontroluje hodnoty při každé změně
            natankuj(objem_l) – kontroluje, zda nedochází k přetečení, a také kontroluje, zda jsou hodnoty smysluplné
            popojed(pocet_km) – kontroluje, zda je dostatek paliva a také zda jsou hodnoty rozumné
    """

