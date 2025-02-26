import tkinter as tk
from constants import WindowColors
from Components.separator import Separator

class Label(tk.Label):
    def __init__(self, parent, text):
        super().__init__(
            parent,
            text=text,
            bg=WindowColors.CODE_EDITOR.value,
            fg="Black",
            font=("Arial", 12, "bold")
        )

class TextEditor(tk.Frame):
    def __init__(self, parent):
        super().__init__(
            parent,
            bg=WindowColors.CODE_EDITOR.value, 
            width=1090, 
            height=510
        )

        self.title = Label(self, "Code Editor")
        self.title.place(x=12, y=12)

        self.spacer = Separator(self, 1060, "Black")
        self.spacer.place(x=8, y=33)

        self.code_text = tk.Text(self, width=132, height=27, bg=WindowColors.CODE_EDITOR.value, fg="Black")
        self.code_text.place(x=8, y=38)

    def clear_editor(self):
        self.code_text.delete("1.0", tk.END)
    
    def insert_code(self, lines):
        self.code_text.insert("1.0",lines)
