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

        self.current_file: str = None

        self.terminal_frame: tk.Frame = None

        self.title: tk.Label = Label(self, "Code Editor")
        self.title.place(x=12, y=12)

        self.spacer: tk.Frame = Separator(self, 1060, "Black")
        self.spacer.place(x=8, y=33)

        self.code_text: tk.Text = tk.Text(self, width=132, height=27, bg=WindowColors.CODE_EDITOR.value, fg="Black", state="disabled", undo="True")
        self.code_text.place(x=8, y=38)

        self.code_text.bind("<Control-s>", self.save_file)
        self.code_text.bind("<Control-l>", self.focus_terminal_frame)

    def save_file(self, event):
        if self.current_file != None:
            code_lines = self.code_text.get("1.0", tk.END).rstrip()
            with open(self.current_file, "w", encoding="utf-8") as f:
                f.write(code_lines)

            self.terminal_frame.show_msg(f"File in the {self.current_file} route saved.")
        else:
            self.terminal_frame.show_error_msg(["not_saved_file"])
    
    def set_terminal_frame(self, terminal_frame: tk.Frame):
        self.terminal_frame = terminal_frame
    
    def set_current_file(self, file_route: str):
        self.current_file = file_route

    def set_title(self, file_name: str):
        self.title.config(text=f"Code Editor - {file_name}")
    
    def enable_editor(self):
        self.code_text.config(state="normal")

    def desable_editor(self):
        self.code_text.config(state="disabled")
    
    def clear_editor(self):
        self.code_text.delete("1.0", tk.END)
    
    def insert_code(self, lines):
        self.code_text.insert("1.0",lines)

    def focus_terminal_frame(self, event):
        self.terminal_frame.focus_terminal()

    def focus_code(self):
        self.code_text.focus_set()
