import time
import threading
import os
class Watcher(threading.Thread):
    """
    Třída Watcher (Producent)
    Odpovědnost: Monitoruje složku a hledá nové soubory.
    Paralelismus: Běží v samostatném vlákně, neblokuje ostatní části programu.
    """
    def __init__(self, directory_to_watch, queue):
        super().__init__()
        # Používáme absolutní cestu pro jistotu
        self.DIRECTORY_TO_WATCH = os.path.abspath(directory_to_watch)
        self.queue = queue
        self.daemon = True # Vlákno se ukončí s hlavním programem

    def run(self):
        # Množina pro sledování již zpracovaných souborů (prevence duplicity)
        seen_files = set()

        while True:
            files = os.listdir(self.DIRECTORY_TO_WATCH)

            for file in files:
                #kontrola duplicity
                if file not in seen_files:
                    seen_files.add(file)
                    print(f"Watcher detected file: {file}")

                    full_path = os.path.join(self.DIRECTORY_TO_WATCH, file)
                    # Vložení do fronty (Thread-safe operace)
                    self.queue.put(full_path)

            # Simulace práce a prevence busy-waiting (vytížení CPU na 100%)
            time.sleep(1)




