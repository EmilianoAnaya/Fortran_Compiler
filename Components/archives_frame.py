import os
import tkinter as tk
from constants import WindowColors, Routes
from Components.separator import Separator

class Title(tk.Label):
    def __init__(self, parent, text):
        super().__init__(
            parent,
            text=text,
            bg=WindowColors.ARCHIVE_BAR.value,
            fg="White"
        )

class FileName(tk.Label):
    def __init__(self, parent, editor_frame, text):
        super().__init__(
            parent,
            text=text,
            bg=WindowColors.ARCHIVE_SELECTOR.value,
            fg="White",
            width=19,
            anchor="w"
        )

        self.text = text
        self.editor_frame = editor_frame
        self.file_route = Routes.COMPILER_FILES.value+self.text

        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)
        self.bind("<Double-Button-1>", self.on_click)

    def on_click(self, event):
        self.editor_frame.clear_editor()
        with open(self.file_route, "r", encoding="utf-8") as f:
            lines = f.read()
        
        self.editor_frame.insert_code(lines)

    def on_enter(self, event):
        self.config(bg="Red")
    
    def on_leave(self, event):
        self.config(bg=WindowColors.ARCHIVE_SELECTOR.value)

class ArchivesFrame(tk.Frame):
    def __init__(self, parent, editor_frame):
        super().__init__(
            parent, 
            width=196,
            height=720,
            bg=WindowColors.ARCHIVE_BAR.value
        )
        self.editor_frame = editor_frame

        self.title = Title(self, text="Archives")
        self.title.place(x=12, y=12)

        self.spacer = Separator(self, 175)
        self.spacer.place(x=8, y=33)

        self.archives_background = tk.Frame(self, width=175, height=670, bg=WindowColors.ARCHIVE_SELECTOR.value)
        self.archives_background.place(x=8, y=40)

        self.archives_container = tk.Frame(self, width=175, height=670, bg=WindowColors.ARCHIVE_SELECTOR.value)
        self.archives_container.place(x=8, y=40)

        self.labels = []

        self.show_files()
    
    def show_files(self):
        self.files = os.listdir(Routes.COMPILER_FILES.value)
        for f in self.files:
            if f != ".gitkeep":
                label = FileName(self.archives_container, self.editor_frame, f)
                label.pack()
                self.labels.append(label)
    
    def clear_files(self):
        for label in self.labels:
            label.destroy()