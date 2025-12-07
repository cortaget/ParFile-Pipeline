from os import mkdir, path
import os
import queue
from Watcher import Watcher
from Loader import Loader
from Mover import Mover
from Logger import Logger
from UI import FolderSelector
import time

if __name__ == '__main__':
    print("Hello, World!")

    DIRECTORY_TO_WATCH = "trash"
    DIRECTORY_TO_SORT = "sorted"
    log_file = "pipeline_log.txt"

    ui = FolderSelector()
    ui.start()
    paths = ui.get_paths()
    number_of_threads = ui.get_number()

    if paths is None or paths[0] is None or paths[1] is None:
        print("Paths were not selected. Shutting down.")
        exit(0)

    DIRECTORY_TO_WATCH, DIRECTORY_TO_SORT = paths
    print(f"Starting monitoring: {DIRECTORY_TO_WATCH}")
    print(f"Sorting to: {DIRECTORY_TO_SORT}")

    # Main script for launching parallel file processing
    q_files = queue.Queue()  # Watcher -> Loader
    q_move = queue.Queue()  # Loader -> Mover
    q_log = queue.Queue()  # Mover -> Logger

    # Create and start threads
    watcher = Watcher(DIRECTORY_TO_WATCH, q_files)
    watcher.start()

    logger = Logger(q_log, log_file)
    logger.start()

    # Can start multiple Loaders for speed!
    for i in range(number_of_threads):  # Start 4 threads
        loader = Loader(DIRECTORY_TO_SORT, q_files, q_move)
        loader.start()

    for i in range(number_of_threads):
        mover = Mover(q_move, q_log)
        mover.start()

    print("Started...")

    # So the script doesn't close immediately
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Terminating application.....")
        q_files.join()
        q_move.join()
        q_log.join()
        print("Done.")
