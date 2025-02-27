import tkinter as tk

class MenuButton(tk.Menu):
    def __init__(self, parent, labels: list[tuple]):
        super().__init__(parent, tearoff=False)
        self.labels: list[tuple] = labels

        for command in self.labels:
            if len(command) > 2:
                sub_menu = tk.Menu(parent, tearoff=False)
                for sub_command in command[2]:
                    sub_menu.add_command(label=sub_command)
                    
                self.add_cascade(label=command[0], menu=sub_menu)
                
            else:    
                self.add_command(
                    label=command[0],
                    accelerator=command[1]
                )

            
                

