from enum import Enum

class WindowColors(Enum):
    MAIN_WINDOW = "#617A4B"
    ARCHIVE_BAR = "#39452F"
    ARCHIVE_SELECTOR = "#1E1E1E"
    CODE_EDITOR = "#8CAA72"
    TERMINAL = "#1C2315"
    NAV_BAR = "#445437"

class Routes(Enum):
    COMPILER_FILES = "Compiler_Files/"
    LIBRARIES = "Data/libraries.json"