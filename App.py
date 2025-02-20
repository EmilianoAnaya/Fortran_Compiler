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
        menu_bar = tk.Menu(bg="#445437")
        file_menu_commands = [("New", "Ctrl+N"), ("Open","Ctrl+A"), ("Clear Screen","Ctrl+P"), ("Close","Ctrl+Q")]
        file_menu = MenuButton(self, file_menu_commands)

        edit_menu_commands = [("Cut","Ctrl+X"), ("Copy", "Ctrl+C"),("Paste", "Ctrl+V"), ("Find","Ctrl+F")]
        edit_menu = MenuButton(self, edit_menu_commands)

        compile_menu_commands = [("Lexic Analisys",None), ("Syntactic Analisys", None),("Semantic Analisys", None), ("Intermediate Code Generation",None),
                                 ("Object Code", None)]
        compile_menu = MenuButton(self, compile_menu_commands)

        help_menu_commands = [("Libraries",None,["stdio.h","conio.h"]), ("Void main", None)]
        help_menu = MenuButton(self, help_menu_commands)

        variables_menu_commands = [("Data Type",None,["int","float","String"])]
        variables_menu = MenuButton(self, variables_menu_commands)

        menu_bar.add_cascade(menu=file_menu, label="File")
        menu_bar.add_cascade(menu=edit_menu, label="Edit")
        menu_bar.add_cascade(menu=compile_menu, label="Compile")
        menu_bar.add_cascade(menu=help_menu, label="Help")
        menu_bar.add_cascade(menu=variables_menu, label="Variables")
        self.config(menu=menu_bar)

        # Frames
        archives_bar_frame = ArchivesFrame(self)
        archives_bar_frame.place(x=0,y=0)

        file_editor_frame = TextEditor(self)
        file_editor_frame.place(x=196,y=0)

        terminal_frame = TerminalFrame(self)
        terminal_frame.place(x=196,y=511)

def main():
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()