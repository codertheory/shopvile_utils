import pathlib
import threading
import tkinter as tk
import traceback
from tkinter import messagebox, ttk

from common import open_file
from modules.inventory_reader import main
from ui.widgets import BrowseButton


class InventoryReaderScreen(tk.Frame):
    def __init__(self,parent: tk.Frame, window: tk.Tk):
        super().__init__(parent)
        self._window: tk.Tk = window
        # Variables to hold file paths
        self.feed_visor_path = tk.StringVar()
        self.inventory_path = tk.StringVar()
        self.restock_report_path = tk.StringVar()

        ## UI elements
        self.run_button: tk.Button = None  # noqa
        self.progress_bar: ttk.Progressbar = None  # noqa


        self.grid(row=1, column=0, padx=10, pady=10)
        self.grid_columnconfigure(0, weight=1)

        # Create UI elements
        self.create_widgets()





    def create_widgets(self):
        browse_feed_visor = BrowseButton(self, "Feed Visor:", self.feed_visor_path)
        browse_feed_visor.grid(row=0, column=0, columnspan=3, padx=5, pady=5, sticky="ew")

        browse_inventory = BrowseButton(self, "Inventory:", self.inventory_path)
        browse_inventory.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky="ew")

        browse_restock = BrowseButton(self, "Restock Report:", self.restock_report_path)
        browse_restock.grid(row=2, column=0, columnspan=3, padx=5, pady=5, sticky="ew")

        self.run_button = tk.Button(self, text="Run", command=self.run_process)
        self.run_button.grid(row=3, column=0, columnspan=4, padx=5, pady=10)

        self.progress_bar = ttk.Progressbar(self, mode="determinate", maximum=10)
        self.progress_bar.grid(
            row=4, column=0, columnspan=4, padx=5, pady=10, sticky="ew"
        )




    def worker(
        self,
        restock_report_path: pathlib.Path,
        inventory_file_path: pathlib.Path,
        feed_visor_processor_path: pathlib.Path,
    ):
        try:
            result = main(
                restock_report_path,
                inventory_file_path,
                feed_visor_processor_path,
                progress_bar=self.progress_bar,
            )
            if result:
                messagebox.showinfo("Process Complete", "File processing is complete.")
                open_file(result)
                self.exit()
        except Exception as e:
            traceback.print_exc()
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            self.run_button.configure(state=tk.NORMAL)

    def run_process(
        self,
    ):
        self.run_button.configure(state=tk.DISABLED)
        try:
            restock_report_path = pathlib.Path(self.restock_report_path.get())
            inventory_file_path = pathlib.Path(self.inventory_path.get())
            feed_visor_processor_path = pathlib.Path(self.feed_visor_path.get())

            if (
                restock_report_path.exists()
                and inventory_file_path.exists()
                and feed_visor_processor_path.exists()
            ):
                # Add your process logic here
                threading.Thread(
                    target=self.worker,
                    daemon=True,
                    kwargs={
                        "restock_report_path": restock_report_path,
                        "inventory_file_path": inventory_file_path,
                        "feed_visor_processor_path": feed_visor_processor_path,
                    },
                ).start()
            else:
                messagebox.showerror(
                    "File Not Found",
                    "One or more files were not found. Please check the paths.",
                )
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

    def exit(self):
        self._window.withdraw()
        self._window.destroy()
