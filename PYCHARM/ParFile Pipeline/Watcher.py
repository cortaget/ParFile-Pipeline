import time
import threading
import os


class Watcher(threading.Thread):
    """
    Watcher Class (Producer)
    Responsibility: Monitors folder and searches for new files.
    Parallelism: Runs in a separate thread, doesn't block other parts of the program.
    """

    def __init__(self, directory_to_watch, queue):
        super().__init__()
        # Using absolute path for certainty
        self.DIRECTORY_TO_WATCH = os.path.abspath(directory_to_watch)
        self.queue = queue
        self.daemon = True  # Thread terminates with main program
        self.sub_watchers = []  # List to store child Watchers

    def run(self):
        # Set to track already processed files (prevents duplicates)
        seen_files = set()

        while True:
            files = os.listdir(self.DIRECTORY_TO_WATCH)

            for file in files:
                # Duplicate check
                if file not in seen_files:
                    seen_files.add(file)
                    full_path = os.path.join(self.DIRECTORY_TO_WATCH, file)

                    # Check if this is a folder
                    if os.path.isdir(full_path):
                        print(f"Watcher detected folder: {file} - starting sub-watcher")
                        # Start new Watcher for this folder
                        sub_watcher = Watcher(full_path, self.queue)
                        sub_watcher.start()
                        self.sub_watchers.append(sub_watcher)
                    else:
                        # This is a file - add to queue for processing
                        print(f"Watcher detected file: {file}")
                        self.queue.put(full_path)

            # Work simulation and busy-waiting prevention (CPU load at 100%)
            time.sleep(1)
