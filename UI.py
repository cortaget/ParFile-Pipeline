import tkinter as tk
from tkinter import filedialog, messagebox
import os
import sys
import threading


class FolderSelector(threading.Thread):

    def __init__(self, file_path="pipeline_log.txt"):
        super().__init__()
        self.file_path = file_path
        self.daemon = False  # Window should work independently
        self.root = None
        self.paths = None
        self.paths_ready = threading.Event()  # Event for synchronization

    def run(self):
        """Launch GUI in separate thread"""
        self.root = tk.Tk()
        self.root.title("ParFile Pipeline - Select Folders")
        self.root.geometry("600x300")

        # Path 1
        tk.Label(self.root, text="Unsorted folder:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_path1 = tk.Entry(self.root, width=50)
        self.entry_path1.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(self.root, text="review", command=lambda: self.browse_folder(self.entry_path1)) \
            .grid(row=0, column=2, padx=5, pady=5)

        # Path 2
        tk.Label(self.root, text="Folder to sort in:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entry_path2 = tk.Entry(self.root, width=50)
        self.entry_path2.grid(row=1, column=1, padx=5, pady=5)
        tk.Button(self.root, text="review", command=lambda: self.browse_folder(self.entry_path2)) \
            .grid(row=1, column=2, padx=5, pady=5)

        # NEW: Number selection
        tk.Label(self.root, text="Number (1-100):").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.number_var = tk.StringVar(value="10")  # Default value
        self.entry_number = tk.Entry(self.root, textvariable=self.number_var, width=10)
        self.entry_number.grid(row=2, column=1, sticky="w", padx=5, pady=5)

        # Submit button
        tk.Button(self.root, text="Submit", command=self.submit_paths, bg="lightgreen") \
            .grid(row=2, column=0, columnspan=3, pady=10)

        # Read logs button
        tk.Button(self.root, text="Read logs", command=self.read_log_file) \
            .grid(row=3, column=0, columnspan=3, pady=5)

        # Stop button
        tk.Button(self.root, text="Stop Pipeline", command=self.stop_pipeline, bg="lightcoral") \
            .grid(row=4, column=0, columnspan=3, pady=5)

        # Label for messages
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
        number_str = self.number_var.get()

        # Number validation
        try:
            number = int(number_str)
            if not 1 <= number <= 100:
                raise ValueError("Number must be between 1 and 100")
        except ValueError:
            self.status_label.config(text="⚠ Enter valid number (1-100)!", fg="red")
            self.root.after(2000, lambda: self.status_label.config(
                text="Waiting for folder selection...", fg="blue"))
            return

        if path1 and path2:
            self.paths = (path1, path2)
            self.number_value = number  # Save selected number
            print("✓ Path 1:", path1)
            print("✓ Path 2:", path2)
            print("✓ Number:", number)
            self.status_label.config(text="✓ Processing started! Window remains open.", fg="green")
            self.paths_ready.set()  # Signal to main.py that paths are ready
        else:
            self.status_label.config(text="⚠ Both paths required!", fg="red")
            self.root.after(2000, lambda: self.status_label.config(
                text="Waiting for folder selection...", fg="blue"))

    def get_paths(self):
        """Waits until user selects paths"""
        self.paths_ready.wait()  # Blocks until paths_ready.set() is called
        return self.paths

    def get_number(self):
        """Returns the number selected by user in UI"""
        if hasattr(self, 'number_value') and self.number_value is not None:
            return self.number_value
        else:
            # If number not selected, return default value
            return 4

    def read_log_file(self):
        """Opens log file in system default program."""
        if os.path.exists(self.file_path):
            try:
                if sys.platform == "win32":  # Windows
                    os.startfile(self.file_path)
                elif sys.platform == "darwin":  # macOS
                    os.system(f"open '{self.file_path}'")
                else:  # Linux
                    os.system(f"xdg-open '{self.file_path}'")
            except Exception as e:
                print(f"Failed to open file: {e}")
        else:
            self.status_label.config(text=f"⚠ Log file not found yet", fg="orange")
            self.root.after(2000, lambda: self.status_label.config(
                text="✓ Processing started! Window remains open.", fg="green"))

    def stop_pipeline(self):
        """Stop pipeline and close program"""
        if self.status_label.cget("text").startswith("✓"):
            result = tk.messagebox.askyesno("Stop Pipeline",
                                            "Are you sure you want to stop the pipeline?")
            if result:
                print("User requested pipeline stop")
                self.root.destroy()
                os._exit(0)  # Force termination of all threads
        else:
            self.root.destroy()

    def on_closing(self):
        """Handle window closing"""
        if self.paths_ready.is_set():
            result = tk.messagebox.askyesno("Exit",
                                            "Pipeline is running. Close anyway?")
            if result:
                self.root.destroy()
                os._exit(0)
        else:
            self.root.destroy()
            os._exit(0)
