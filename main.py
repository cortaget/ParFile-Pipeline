from os import mkdir, path
import os
import queue
from Watcher import Watcher
from Loader import Loader
from Mover import Mover
from Logger import Logger
import time

if __name__ == '__main__':
    print ("Hello, World!")


    files = os.listdir("trash")
    print(files)

    """Hlavní skript pro spuštění paralelního zpracování souborů."""

    q_files = queue.Queue()  # Watcher -> Loader
    q_move = queue.Queue()  # Loader -> Mover
    q_log = queue.Queue()  # Mover -> Logger

    DIRECTORY_TO_WATCH = "trash"
    DIRECTORY_TO_Sort = "sorted"
    log_file = "pipeline_log.txt"

    # Создаем и запускаем потоки
    watcher = Watcher(DIRECTORY_TO_WATCH, q_files)
    watcher.start()

    logger = Logger(q_log, log_file)
    logger.start()

    # Можно запустить несколько Loader-ов для скорости!
    for i in range(4):  # Запускаем 4 потока
        loader = Loader(DIRECTORY_TO_Sort,q_files, q_move, )
        loader.start()

    for i in range(4):
        mover = Mover(q_move, q_log)
        mover.start()

    print("Zapnuto...")


    # Чтобы скрипт не закрылся сразу
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Ukončování aplikace.....")
        q_files.join()
        q_move.join()
        q_log.join()
        print("Hotovo.")



