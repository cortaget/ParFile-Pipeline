Parallel File Sorter - Dokumentace Projektu
Název projektu:	Parallel File Sorter
Autor:	[Vaše Jméno]
Datum:	23.11.2025
Škola:	[Název vaší školy]
Předmět:	Paralelní programování
Typ projektu:	Školní projekt (Vzdělávací software)
📋 Obsah

    Specifikace požadavků

    Architektura aplikace

    Popis běhu (Behaviorální model)

    Rozhraní a závislosti

    Instalace a spuštění

    Konfigurace

    Právní a licenční aspekty

    Chybové stavy

    Testování a validace

    Verze a známé chyby

1. Specifikace požadavků
Cíl projektu

Vytvořit aplikaci pro automatické třídění souborů v reálném čase s využitím paralelního zpracování, která demonstruje řešení problému Producer-Consumer.
Business Requirements (BR)

    BR1: Aplikace musí ušetřit čas uživatele automatizací organizace souborů.

    BR2: Aplikace musí být schopna zpracovat velký nápor dat bez zamrznutí.

Functional Requirements (FR)

    FR1 (Monitoring): Aplikace nepřetržitě sleduje vstupní složku trash.

    FR2 (Detekce): Identifikuje nové soubory a ignoruje již zpracované.

    FR3 (Třídění): Automaticky vytváří složky podle přípony souboru (např. sorted_JPG).

    FR4 (Paralelismus): Procesy detekce, analýzy a přesunu běží souběžně.

Non-Functional Requirements (NFR)

    NFR1: Využití jazyka Python a knihovny threading.

    NFR2: Bezpečné předávání dat mezi vlákny (Thread-safety).

    NFR3: Robustnost vůči I/O chybám (např. smazání souboru během procesu).

2. Architektura aplikace

Aplikace využívá návrhový vzor Pipeline se třemi fázemi zpracování.
Komponenty ("Big Picture")

    Watcher (Producent):

        Odpovědnost: I/O operace (skenování disku).

        Výstup: Cesty k souborům -> Queue 1.

    Loader (Processor):

        Odpovědnost: Logika (parsování přípony, tvorba složek).

        Vstup: Queue 1 -> Výstup: Příkaz k přesunu -> Queue 2.

        Běží ve 4 instancích.

    Mover (Konzument):

        Odpovědnost: I/O operace (fyzický přesun dat).

        Vstup: Queue 2.

        Běží ve 4 instancích.

Schéma vazeb

text
[File System] --> (Watcher) --[Queue 1]--> (Loaders x4) --[Queue 2]--> (Movers x4) --> [File System]

3. Popis běhu (Behaviorální model)

Typický životní cyklus zpracování jednoho souboru (Use Case):
UML Diagram aktivit pro zpracování souboru (Activity Diagram)
UML Diagram aktivit pro zpracování souboru (Activity Diagram)

    Start: Uživatel nahraje soubor do složky.

    Detekce: Watcher jej najde, ověří v cache seen_files a pošle do fronty.

    Analýza: Loader si soubor vyzvedne. Zjistí typ .pdf.

    Příprava: Loader ověří existenci složky sorted_PDF. Pokud není, vytvoří ji (atomicky).

    Přesun: Mover obdrží příkaz a přesune soubor.

    Konec: Soubor je na novém místě.

4. Rozhraní a závislosti
Závislosti (Third-party libraries)

Projekt je navržen s minimálními závislostmi pro snadnou přenositelnost.

    Python Standard Library:

        threading: Správa paralelních vláken.

        queue: Synchronizovaná fronta (Thread-safe FIFO).

        os, shutil: Manipulace se souborovým systémem.

        time: Řízení cyklů.

Hardwarové požadavky

    OS: Windows 10/11, Linux, macOS.

    CPU: Vícejádrový procesor doporučen pro efektivní I/O operace.

    RAM: Minimální nároky (~50 MB).

5. Instalace a spuštění
Instalace

Aplikace nevyžaduje instalaci. Je distribuována jako "portable" skript.
Spuštění

    Ujistěte se, že máte nainstalován Python 3.8+.

    Stáhněte zdrojový kód projektu.

    V terminálu přejděte do složky projektu.

    Spusťte příkaz:

    bash
    python main.py

    Aplikace automaticky vytvoří složky trash (vstup) a sorted (výstup).

6. Konfigurace

Konfigurace je definována přímo v souboru main.py (Hard-coded configuration pro zjednodušení školního projektu).

Možnosti úprav (v kódu):

    num_loaders = 4: Počet vláken pro analýzu souborů. Zvyšte pro systémy s rychlým CPU.

    num_movers = 4: Počet vláken pro přesun. Zvyšte pro systémy s rychlým SSD.

    time.sleep(1) ve Watcheru: Interval skenování složky (v sekundách).

7. Právní a licenční aspekty

    Licence: MIT License (Open Source).

    Autorská práva: Kód je duševním vlastnictvím autora uvedeného v hlavičce.

    Prohlášení: Tento software je školní projekt. Autor nenese odpovědnost za případnou ztrátu dat při nesprávném použití aplikace na citlivých souborech.

8. Chybové stavy
Kód chyby / Výjimka	Příčina	Chování aplikace
FileNotFoundError	Soubor byl smazán uživatelem před zpracováním.	Zalagováno do konzole, vlákno pokračuje dál.
PermissionError	Aplikace nemá práva k zápisu.	Vypsána chyba, soubor je přeskočen.
FileExistsError	Cílový soubor již existuje.	Operační systém může vyvolat chybu, soubor zůstane ve vstupní složce.
9. Testování a validace

Aplikace byla validována pomocí integračních testů.

Testovací scénář TC-01 (Souběžnost):

    Akce: Vložení 50 souborů najednou.

    Výsledek: Všechna vlákna (Loaders/Movers) se aktivovala. Soubory byly roztříděny do 2 sekund. Žádný soubor se neztratil.

    Status: ✅ Úspěch

Testovací scénář TC-02 (Duplicita):

    Akce: Watcher běží 10 minut se stejnými soubory ve složce.

    Výsledek: Soubory byly přidány do fronty pouze jednou (díky seen_files). Paměť nerostla.

    Status: ✅ Úspěch
