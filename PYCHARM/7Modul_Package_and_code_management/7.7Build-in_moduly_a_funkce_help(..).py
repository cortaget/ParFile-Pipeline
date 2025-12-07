import sys

# Seznam modulů a popis
modules = [
    ("csv", "Čtení a zápis CSV souborů"),
    ("openpyxl", "Čtení a zápis XLSX souborů (externí)"),
    ("mysql.connector", "Připojení k MySQL databázi (externí)"),
    ("zipfile", "Vytvoření a čtení ZIP archivu"),
    ("platform", "Zjištění verze a typu OS"),
    ("math", "Výpočet logaritmu, funkce log10"),
    ("json", "Parsování JSON"),
    ("sqlparse", "Parsování SQL (externí)"),
    ("socket", "Zjištění IP adresy a síťových informací"),
    ("fpdf", "Generování PDF (externí)")
]

for mod_name, description in modules:
    print("\n" + "=" * 50)
    print(f"Modul: {mod_name} - {description}")

    try:
        # Dynamický import
        mod = __import__(mod_name)
        print("Obsah modulu (dir()):")
        print(dir(mod))
        print("\nDokumentace (help()):")
        # Pro built-in moduly můžeme vypsat help
        if mod_name in ["csv", "zipfile", "platform", "math", "json", "socket"]:
            help(mod)
        else:
            print("Help vyžaduje externí modul, který musí být nainstalován.")
    except ModuleNotFoundError:
        print(f"Modul {mod_name} není nainstalován.")


