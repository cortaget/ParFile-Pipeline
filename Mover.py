import threading
from managment.file_manager import move_file_to_folder


class Mover(threading.Thread):
    """
    Mover Class (Consumer)
    Responsibility: Physically moves files.
    Parallelism: Separates slow disk operations from sorting logic.
    """

    def __init__(self, in_queue, out_queue):
        super().__init__()
        self.queue = in_queue
        self.out_queue = out_queue
        self.daemon = True

    def run(self):
        while True:
            # Pick up task (source, destination) from queue
            file_path, destination_folder = self.queue.get()

            try:
                # Critical I/O operation - move file
                move_file_to_folder(file_path, destination_folder)
                self.out_queue.put(f"Moved file '{file_path}' to '{destination_folder}'")

            except PermissionError:
                print(f"Permission denied when moving file '{file_path}' to '{destination_folder}'")
                self.out_queue.put(
                    f"Error message '{file_path}' to '{destination_folder}'(The file is currently being used by another program. Turn off the program that is using the file and restart the file sorting program.) ")

            except Exception as e:
                print(f"Error moving file '{file_path}' to '{destination_folder}': {e}")
                self.out_queue.put(f"Error moving file '{file_path}' to '{destination_folder}': {e}")

            finally:
                self.queue.task_done()