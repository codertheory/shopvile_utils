import tkinter as tk
from tkinter import filedialog


class BrowseButton(tk.Frame):
    def __init__(self, parent: tk.Frame, label_text: str, variable: tk.StringVar):
        super().__init__(parent)
        self.variable = variable

        self.label = tk.Label(self, text=label_text, width=10)
        self.label.grid(row=0, column=0, padx=5, pady=5)

        self.entry = tk.Entry(self, textvariable=self.variable, width=100)
        self.entry.grid(row=0, column=1, padx=5, pady=5)

        self.button = tk.Button(self, text="Browse", command=self.browse)
        self.button.grid(row=0, column=2, padx=5, pady=5)

        self.grid_columnconfigure(1, weight=1)

    def browse(self):
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            self.variable.set(file_path)
