import os
import tkinter as tk
from constants import WindowColors, Routes
from Components.separator import Separator
from Tools.lexic_analyzer import LexicAnalyzer

class Label(tk.Label):
    def __init__(self, parent, text):
        super().__init__(
            parent,
            text=text,
            bg=WindowColors.TERMINAL.value,
            fg="White"
        )

class TerminalFrame(tk.Frame):
    def __init__(self, parent, archives_frame, code_frame):
        super().__init__(
            parent,
            bg=WindowColors.TERMINAL.value, 
            width=1090, 
            height=210
        )
        self.parent: tk.Tk = parent
        self.archive_frame: tk.Frame = archives_frame
        self.code_frame: tk.Frame = code_frame

        self.error_flag: bool = False
        self.terminal_index: int = -1
        self.terminal_commands: list = []

        self.title: tk.Label = Label(self, text="Terminal")
        self.title.place(x=12, y=12)

        self.commands: dict = {
            "clear" : self.clear_terminal,
            "touch" : self.create_file,
            "exit" : self.finish_app,
            "lexic_analyzer" : self.lexic_analyzer
        }

        self.error_msg: dict = {
            "main_command" : "Error, command not valid",
            "params" : {
                "no_params" : "No params detected when creating file",
                "many_params" : "Too many arguments, expected 1",
            },
            "not_saved_file" : "Error while saving, no file has been selected",
            "file_not_found" : "The file to use was not found"
        }

        self.spacer: tk.Frame = Separator(self, 1060)
        self.spacer.place(x=8, y=33)

        self.input_terminal: tk.Text = tk.Text(self, width=132, height=9, bg=WindowColors.TERMINAL.value, fg="White")
        self.input_terminal.insert("end", ":/> ")
        self.input_terminal.place(x=8, y=36)
        
        self.input_terminal.bind("<Return>", self.on_enter)
        self.input_terminal.bind("<BackSpace>", self.on_delete)
        self.input_terminal.bind("<Left>", self.on_delete)
        self.input_terminal.bind("<Up>", lambda e: "break")
        self.input_terminal.bind("<Down>", lambda e: "break")

        self.input_terminal.bind("<Control-l>", self.focus_code_frame)

        self.Lexic_analyzer = LexicAnalyzer(self)
    
    def finish_app(self):
        self.error_flag = True
        self.parent.close_app()
    
    def clear_terminal(self):
        self.input_terminal.delete("1.0", tk.END)
    
    def on_delete(self, event):
        _, current_index = self.input_terminal.index(tk.INSERT).split(".")
        if int(current_index) == 4:
            return "break"
    
    def new_line(self):
        self.input_terminal.insert("end", "\n:/> ")
    
    def focus_code_frame(self, event):
        self.code_frame.focus_code()
    
    def focus_terminal(self):
        self.input_terminal.focus_set()
    
    def show_line(self, line:str):
        self.input_terminal.insert("end", f"\n{line}")
    
    def show_msg(self, msg: str):
        self.input_terminal.insert("end", f"\n{msg}")
        self.new_line()
    
    def show_error_msg(self,params: list):
        self.error_flag = True
        main_msg = self.error_msg
        for param in params:
            main_msg = main_msg[param] 
        
        self.input_terminal.insert("end", f"\n{main_msg}")
        self.new_line()

    def get_current_line(self):
        current_line, _ = self.input_terminal.index(tk.INSERT).split(".")
        row = self.input_terminal.get(f"{current_line}.4", f"{current_line}.end")
        return row
    
    def commands_shortcut(self, event, index):
        self.terminal_index =+ index
        final_index = len(self.terminal_commands)-1
        if self.terminal_index <= -1:
            self.terminal_index = -1
            # Limpiar la línea sin salto de línea
        elif self.terminal_index > final_index:
            self.terminal_index = final_index
        command = self.terminal_commands[self.terminal_index]
        
    
    def params_checker(self, args) -> bool:
        if args == None:
            self.show_error_msg(["params","no_params"])
            return False
        
        if len(args) > 1:
            self.show_error_msg(["params","many_params"])
            return False
        
        return True
    
    def on_enter(self, event):
        self.error_flag = False
        row = self.get_current_line()
        if row != "":
            main_command = row.split()[0]
            args = row.split()[1:] if row.split()[1:] != [] else None
            if main_command in self.commands:
                if args == None:
                    self.commands[main_command]()
                else:
                    self.commands[main_command](args)
            elif main_command != "":
                self.show_error_msg(["main_command"])
        
        if not self.error_flag:
            self.new_line()
            return "break"
        else:
            return "break"  

    def create_file(self, args=None):
        if not self.params_checker(args):
            return
        file_name = args[0]
        if file_name[-4:] != ".f90":
            file_name +=".f90"
        
        file_route = os.path.join(Routes.COMPILER_FILES.value, file_name)
        open(file_route, "w").close()

        self.archive_frame.clear_files()
        self.archive_frame.show_files()

    def lexic_analyzer(self, args=None):
        if not self.params_checker(args):
            return
        file_name = args[0]
        file_route = os.path.join(Routes.COMPILER_FILES.value, file_name)
        try:
            with open(file_route, "r", encoding="utf-8") as f:
                lines = f.read()
            self.Lexic_analyzer.parse(lines)
                
        except FileNotFoundError:
            self.show_error_msg(["file_not_found"])

