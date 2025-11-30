import tkinter as tk
from tkinter import filedialog, messagebox
import os
import sys
import threading


class FolderSelector(threading.Thread):
    def __init__(self, file_path="pipeline_log.txt"):
        super().__init__()
        self.file_path = file_path
        self.daemon = False  # Окно должно работать независимо

        self.root = None
        self.paths = None
        self.paths_ready = threading.Event()  # Событие для синхронизации

    def run(self):
        """Запуск GUI в отдельном потоке"""
        self.root = tk.Tk()
        self.root.title("ParFile Pipeline - Select Folders")
        self.root.geometry("600x250")

        # Путь 1
        tk.Label(self.root, text="Unsorted folder:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_path1 = tk.Entry(self.root, width=50)
        self.entry_path1.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(self.root, text="review", command=lambda: self.browse_folder(self.entry_path1)) \
            .grid(row=0, column=2, padx=5, pady=5)

        # Путь 2
        tk.Label(self.root, text="Folder to sort in:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entry_path2 = tk.Entry(self.root, width=50)
        self.entry_path2.grid(row=1, column=1, padx=5, pady=5)
        tk.Button(self.root, text="review", command=lambda: self.browse_folder(self.entry_path2)) \
            .grid(row=1, column=2, padx=5, pady=5)

        # Кнопка отправки
        tk.Button(self.root, text="Submit", command=self.submit_paths, bg="lightgreen") \
            .grid(row=2, column=0, columnspan=3, pady=10)

        # Кнопка чтения логов
        tk.Button(self.root, text="Read logs", command=self.read_log_file) \
            .grid(row=3, column=0, columnspan=3, pady=5)

        # Кнопка остановки
        tk.Button(self.root, text="Stop Pipeline", command=self.stop_pipeline, bg="lightcoral") \
            .grid(row=4, column=0, columnspan=3, pady=5)

        # Label для сообщения
        self.status_label = tk.Label(self.root, text="Waiting for folder selection...", fg="blue")
        self.status_label.grid(row=5, column=0, columnspan=3, pady=10)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def browse_folder(self, entry):
        folder_path = filedialog.askdirectory()
        if folder_path:
            entry.delete(0, tk.END)
            entry.insert(0, folder_path)

    def submit_paths(self):
        path1 = self.entry_path1.get()
        path2 = self.entry_path2.get()

        if path1 and path2:
            self.paths = (path1, path2)
            print("✓ Путь 1:", path1)
            print("✓ Путь 2:", path2)
            self.status_label.config(text="✓ Processing started! Window remains open.", fg="green")
            self.paths_ready.set()  # Сигнал main.py, что пути готовы
        else:
            self.status_label.config(text="⚠ Both paths required!", fg="red")
            self.root.after(2000, lambda: self.status_label.config(
                text="Waiting for folder selection...", fg="blue"))

    def get_paths(self):
        """Ждёт, пока пользователь не выберет пути"""
        self.paths_ready.wait()  # Блокирует до вызова paths_ready.set()
        return self.paths

    def read_log_file(self):
        """Открывает файл логов в стандартной программе системы."""
        if os.path.exists(self.file_path):
            try:
                if sys.platform == "win32":  # Windows
                    os.startfile(self.file_path)
                elif sys.platform == "darwin":  # macOS
                    os.system(f"open '{self.file_path}'")
                else:  # Linux
                    os.system(f"xdg-open '{self.file_path}'")
            except Exception as e:
                print(f"Не удалось открыть файл: {e}")
        else:
            self.status_label.config(text=f"⚠ Log file not found yet", fg="orange")
            self.root.after(2000, lambda: self.status_label.config(
                text="✓ Processing started! Window remains open.", fg="green"))

    def stop_pipeline(self):
        """Остановка pipeline и закрытие программы"""
        if self.status_label.cget("text").startswith("✓"):
            result = tk.messagebox.askyesno("Stop Pipeline",
                                            "Are you sure you want to stop the pipeline?")
            if result:
                print("User requested pipeline stop")
                self.root.destroy()
                os._exit(0)  # Принудительное завершение всех потоков
        else:
            self.root.destroy()

    def on_closing(self):
        """Обработка закрытия окна"""
        if self.paths_ready.is_set():
            result = tk.messagebox.askyesno("Exit",
                                            "Pipeline is running. Close anyway?")
            if result:
                self.root.destroy()
                os._exit(0)
        else:
            self.root.destroy()
            os._exit(0)
