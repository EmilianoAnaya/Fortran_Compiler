import tkinter as tk
from Components.menu_button import MenuButton
from Components.archives_frame import ArchivesFrame
from Components.terminal_frame import TerminalFrame
from Components.text_editor import TextEditor
from constants import WindowColors

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Fortran Compiler")
        self.geometry("1280x720")
        self.resizable(False, False)
        self.configure(bg=WindowColors.MAIN_WINDOW.value)

        # Menu Bar
        self.menu_bar: tk.Menu = tk.Menu(bg="#445437")
        self.file_menu_commands: list[tuple] = [("New", "Ctrl+N"), ("Open","Ctrl+A"), ("Clear Screen","Ctrl+P"), ("Close","Ctrl+Q")]
        self.file_menu: tk.Menu = MenuButton(self, self.file_menu_commands)

        self.edit_menu_commands: list[tuple] = [("Cut","Ctrl+X"), ("Copy", "Ctrl+C"),("Paste", "Ctrl+V"), ("Find","Ctrl+F")]
        self.edit_menu: tk.Menu = MenuButton(self, self.edit_menu_commands)

        self.compile_menu_commands: list[tuple] = [("Lexic Analisys",None), ("Syntactic Analisys", None),("Semantic Analisys", None), ("Intermediate Code Generation",None),
                                ("Object Code", None)]
        self.compile_menu: tk.Menu = MenuButton(self, self.compile_menu_commands)

        self.help_menu_commands: list[tuple] = [("Libraries",None,["stdio.h","conio.h"]), ("Void main", None)]
        self.help_menu: tk.Menu = MenuButton(self, self.help_menu_commands)

        self.variables_menu_commands: list[tuple] = [("Data Type",None,["int","float","String"])]
        self.variables_menu: tk.Menu = MenuButton(self, self.variables_menu_commands)

        self.menu_bar.add_cascade(menu=self.file_menu, label="File")
        self.menu_bar.add_cascade(menu=self.edit_menu, label="Edit")
        self.menu_bar.add_cascade(menu=self.compile_menu, label="Compile")
        self.menu_bar.add_cascade(menu=self.help_menu, label="Help")
        self.menu_bar.add_cascade(menu=self.variables_menu, label="Variables")
        self.config(menu=self.menu_bar)

        # Frames
        self.file_editor_frame: tk.Frame = TextEditor(self)
        self.file_editor_frame.place(x=196,y=0)

        self.archives_bar_frame: tk.Frame = ArchivesFrame(self, self.file_editor_frame)
        self.archives_bar_frame.place(x=0,y=0)

        self.terminal_frame: tk.Frame = TerminalFrame(self, 
                                                    self.archives_bar_frame, 
                                                    self.file_editor_frame)
        self.terminal_frame.place(x=196,y=511)

        self.file_editor_frame.set_terminal_frame(self.terminal_frame)

    def close_app(self):
        self.destroy()

def main():
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()