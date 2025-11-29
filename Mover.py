import threading
from managment.file_manager import move_file_to_folder

class Mover(threading.Thread):
    """
    Třída Mover (Konzument)
    Odpovědnost: Fyzicky přesouvá soubory.
    Paralelismus: Odděluje pomalé diskové operace od logiky třídění.
    """
    def __init__(self, in_queue,out_queue):
        super().__init__()
        self.queue = in_queue
        self.out_queue = out_queue
        self.daemon = True

    def run(self):
        while True:
            # Vyzvednutí úkolu (zdroj, cíl) z fronty
            file_path, destination_folder = self.queue.get()
            try:


                # Kritická I/O operace - přesun souboru
                move_file_to_folder(file_path, destination_folder)
                #print(f"Moved file '{file_path}' to '{destination_folder}'")
                self.out_queue.put(f"Moved file '{file_path}' to '{destination_folder}'")


            except PermissionError:
                print(f"Permission denied when moving file '{file_path}' to '{destination_folder}'")
                self.out_queue.put(f"Error message '{file_path}' to '{destination_folder}'(The file is currently being used by another program. Turn off the program that is using the file and restart the file sorting program.) ")
            except Exception as e:
                print(f"Error moving file '{file_path}' to '{destination_folder}': {e}")
                self.out_queue.put(f"Error moving file '{file_path}' to '{destination_folder}': {e}")
            finally:
                self.queue.task_done()