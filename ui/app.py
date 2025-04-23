import tkinter as tk

from ui.constants import selectionbar_color
from ui.screens.inventory_excluder_screen import InventoryExcluderScreen
from ui.screens.inventory_reader_screen import (
    InventoryReaderScreen,
)
from ui.sidebar import Sidebar

# ------------------------------- ROOT WINDOW ----------------------------------


class ShopVilleUiApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # ------------- BASIC APP LAYOUT -----------------
        self.title("Shopville Utility App")
        self.geometry("1100x700")
        self.config(background=selectionbar_color)
        self.resizable(width=False, height=False)
        self.eval("tk::PlaceWindow . center")
        icon = tk.PhotoImage(file="ui/assets/logo.png")
        self.iconphoto(True, icon)

        # --------------------  MAIN FRAME ---------------------------

        main_frame = tk.Frame(self)
        main_frame.place(relx=0.2, relwidth=1)

        # --------------------  SIDEBAR SETTINGS ----------------------------
        Sidebar(
            self,
            icon,
            frame_cb=self.show_frame,
            options=[
                {
                    "name": "Inventory Reader",
                    "icon": "ui/assets/icons/Frame1.png",
                    "frame": InventoryReaderScreen,
                },
                {
                    "name": "Inventory Excluder",
                    "icon": "ui/assets/icons/Frame2.png",
                    "frame": InventoryExcluderScreen,
                },
            ],
        )

        # --------------------  MULTI PAGE SETTINGS ----------------------------

        container = tk.Frame(self)
        container.config(highlightbackground="#808080", highlightthickness=0.4)
        container.place(relx=0.2, relwidth=0.8, relheight=1)

        self.frames = {}

        for F in (
            InventoryReaderScreen,
            InventoryExcluderScreen,
        ):
            frame = F(container, self)
            self.frames[F] = frame
            frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.show_frame(InventoryReaderScreen)

    def show_frame(self, cont):
        """
        this function enable us to switch between frames
        """
        frame = self.frames[cont]
        frame.tkraise()
