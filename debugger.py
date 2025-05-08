from Tools.automaton import Compiler
from constants import WindowColors, Routes
import os

def main():
    terminal = "hi"
    file_name: str = "functions_example.f90"
    # file_name: str = "while_structure.f90"
    # file_name: str = "if_then_else.f90"
    compiler = Compiler(terminal, True)
    file_route = os.path.join(Routes.COMPILER_FILES.value, file_name)
    try:
        with open(file_route, "r", encoding="utf-8") as f:
            lines = [line.strip() for line in f]
        
        compiler.reset_all()

        program_name: str = file_name.replace(".f90", "")
        compiler.compile(lines, program_name)
            
    except FileNotFoundError:
        print(["file_not_found"])

if __name__ == "__main__":
    main()
