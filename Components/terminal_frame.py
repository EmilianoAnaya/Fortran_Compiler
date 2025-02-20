import tkinter as tk
from constants import WindowColors
from Components.separator import Separator

class Label(tk.Label):
    def __init__(self, parent, text):
        super().__init__(
            parent,
            text=text,
            bg=WindowColors.TERMINAL.value,
            fg="White"
        )

class TerminalFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(
            parent,
            bg=WindowColors.TERMINAL.value, 
            width=1090, 
            height=210
        )
        self.title = Label(self, text="Terminal")
        self.title.place(x=12, y=12)

        self.spacer = Separator(self, 1060)
        self.spacer.place(x=8, y=33)

        self.input_terminal = tk.Text(self, width=132, height=9, bg=WindowColors.TERMINAL.value, fg="White")
        self.input_terminal.insert("end", ":/> ")
        
        self.input_terminal.bind("<Return>", self.on_enter)
        self.input_terminal.place(x=8, y=36)

    def on_enter(self, event):
        self.input_terminal.insert("end", "\n:/> ")
        return "break"