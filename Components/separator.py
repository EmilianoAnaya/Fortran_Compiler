import tkinter as tk

class Separator(tk.Frame):
    def __init__(self, parent, size, color="White"):
        super().__init__(
            parent,
            width=size,
            height=2,
            bg=color
        )