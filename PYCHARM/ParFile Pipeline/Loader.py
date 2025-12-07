import threading
from managment.file_manager import get_file_suffix
from managment.folder_manager import create_folder
import os


class Loader(threading.Thread):
    """
    Loader Class (Consumer & Producer)
    Responsibility: Processes files from queue, determines their type and prepares target folders.
    Parallelism: Can run in multiple instances to speed up sorting.
    """

    def __init__(self, DIRECTORY_TO_Sort, in_queue, out_queue):
        super().__init__()
        self.queue = in_queue  # Input queue from Watcher
        self.out_queue = out_queue  # Output queue for Mover
        self.DIRECTORY_TO_Sort = DIRECTORY_TO_Sort
        self.daemon = True  # Thread terminates with main program

    def run(self):
        while True:
            # Blocking call - waits for data from queue
            file_path = self.queue.get()

            try:
                suffix = get_file_suffix(file_path)
                # FIXED: Folder is created INSIDE the selected directory
                target_folder = os.path.join(self.DIRECTORY_TO_Sort, suffix[1:].upper())

                # Create folder for given format if it doesn't exist
                if not os.path.isdir(target_folder):
                    create_folder(target_folder)

                task = (file_path, target_folder)
                # Pass task forward to "shipping" queue
                self.out_queue.put(task)

            except Exception as e:
                print(f"Error processing file '{file_path}': {e}")
            finally:
                # Signal that task from queue is completed
                self.queue.task_done()

    def test(self, file_path):
        suffix = get_file_suffix(file_path)
        format_exist = os.path.isdir(f"sorted/sorted_{suffix[1:].upper()}")

        if not format_exist:
            create_folder(f"sorted/sorted_{suffix[1:].upper()}")


if __name__ == '__main__':
    loader = Loader()
    loader.test('trash/images.jpg')
