import threading
from datetime import datetime
import re

class Logger(threading.Thread):
    def __init__(self, in_queue,logfile):
        super().__init__()
        self.logfile = logfile
        self.queue = in_queue # Vstupní fronta od Watchera
        self.daemon = True




    def run(self):
        while True:
            # Blokující volání - čeká na data z fronty
            log_message = self.queue.get()
            try:
                if re.search('Moved file',log_message):
                    self.info(f"Log message: {log_message}")
                elif re.search('Error message',log_message):
                    self.error(f"Error message: {log_message}")


            except Exception as e:
                print(f"Error logging message '{log_message}': {e}")
                self.error(f"Error logging message '{log_message}': {e}")
            finally:
                # Signalizace, že úkol z fronty byl dokončen
                self.queue.task_done()

    def log(self, message):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] {message}\n"

        # Просто добавляем в конец (быстро и безопасно)
        with open(self.logfile, 'a', encoding='utf-8') as f:
            f.write(log_entry)

    def info(self, message):
        self.log(f"[INFO] {message}")

    def error(self, message):
        self.log(f"[ERROR] {message}")