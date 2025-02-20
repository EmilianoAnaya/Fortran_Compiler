import tkinter as tk
from constants import WindowColors
from Components.separator import Separator

class Label(tk.Label):
    def __init__(self, parent, text):
        super().__init__(
            parent,
            text=text,
            bg=WindowColors.ARCHIVE_BAR.value,
            fg="White"
        )

class ArchivesFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(
            parent, 
            width=196,
            height=720,
            bg=WindowColors.ARCHIVE_BAR.value
        )
        self.title = Label(self, text="Archives")
        self.title.place(x=12, y=12)

        self.spacer = Separator(self, 178)
        self.spacer.place(x=8, y=33)

        self.archives_container = tk.Frame(self, width=178, height=670, bg=WindowColors.ARCHIVE_SELECTOR.value)
        self.archives_container.place(x=8, y=40)
