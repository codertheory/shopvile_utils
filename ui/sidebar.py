import pathlib
import tkinter as tk
import typing
from tkinter import ttk
from typing import TypedDict
from ui.constants import sidebar_color


class SideBarOption(typing.TypedDict):
    """
    This is a dictionary which will hold the options for the sidebar.
    The keys are the names of the options and the values are the functions
    which will be called when the option is clicked.
    """

    name: str
    icon: pathlib.Path
    frame: type[tk.Frame]


class Sidebar(tk.Frame):
    """
    A sidebar which can have multiple options and these can be linked with
    functions.
    """

    def __init__(
        self,
        parent,
        options: list[dict],
        frame_cb: callable = None,
    ):
        """
        This is the constructor for the Sidebar class.
        :param parent: The parent frame
        :param options: The options to be displayed in the sidebar
        :param frame_cb: The function to be called when an option is clicked
        """
        super().__init__(parent, bg=sidebar_color)
        self.place(relx=0, rely=0, relwidth=0.2, relheight=1)
        self.frame_cb = frame_cb
        self.grid_columnconfigure(0, weight=1)
        for i, option in enumerate(options):
            btn = tk.Button(
                self,
                text=option["name"],
                command=lambda opt=option["frame"]: self.on_option_click(opt),
            )
            btn.place(relx=0, rely=0, relwidth=1, relheight=1)
            btn.grid(row=i, column=0, sticky="ew", padx=5, pady=5)

    def on_option_click(self, option):
        """
        This function is called when an option is clicked.
        It will call the function linked with the option.
        """
        if self.frame_cb:
            self.frame_cb(option)
