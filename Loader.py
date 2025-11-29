import threading
from managment.file_manager import get_file_suffix
from  managment.folder_manager import create_folder
import os



class Loader(threading.Thread):
    """
    Třída Loader (Konzument & Producent)
    Odpovědnost: Zpracovává soubory z fronty, určuje jejich typ a připravuje cílové složky.
    Paralelismus: Může běžet ve více instancích pro zrychlení třídění.
    """
    def __init__(self,DIRECTORY_TO_Sort,in_queue,out_queue):
        super().__init__()

        self.queue = in_queue # Vstupní fronta od Watchera
        self.out_queue = out_queue # Výstupní fronta pro Movera
        self.daemon = True



    def run(self):
        while True:
            # Blokující volání - čeká na data z fronty
            file_path = self.queue.get()
            try:
                suffix = get_file_suffix(file_path)

                format_exist = os.path.isdir(f"sorted/sorted_{suffix[1:].upper()}")
                # Vytvoření složky pro daný formát, pokud neexistuje
                if not format_exist:
                    create_folder(f"sorted/sorted_{suffix[1:].upper()}")

                task = (file_path, f"sorted/sorted_{suffix[1:].upper()}/")
                # Předání úkolu dál do "expediční" fronty
                self.out_queue.put(task)



            except Exception as e:
                print(f"Error processing file '{file_path}': {e}")
            finally:
                # Signalizace, že úkol z fronty byl dokončen
                self.queue.task_done()



    def test(self,file_path):

        suffix = get_file_suffix(file_path)

        format_exist = os.path.isdir(f"sorted/sorted_{suffix[1:].upper()}")

        if not format_exist:
            create_folder(f"sorted/sorted_{suffix[1:].upper()}")


if __name__ == '__main__':
    loader = Loader()
    loader.test('trash/images.jpg')



