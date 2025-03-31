import re

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Tools.automaton import Compiler

class IfStructure():
    def __init__(self, temporal_code: list[str], compiler):
        self.temporal_code: list[str] = temporal_code
        self.compiler: Compiler = compiler
        
        self.ignore_if_sections: bool = True
        self.if_section_done: bool = False

        self.ignore_code: bool = False
        self.ignore_index: int = -1

        self.ifs_counter: int = 0
    
    def check_end_if(self, line: str):
        formatted_line = " ".join(line)
        current_if_index = self.temporal_code.index(formatted_line)
        if_pile = 0
        tmp_code: list[str] = []
        pattern = r"if\s*\(\s*[^()]+\s*\)\s*then"

        for i in range(current_if_index, len(self.temporal_code)):
            tmp_code.append(self.temporal_code[i])
            if re.fullmatch(pattern, self.temporal_code[i]):
                if_pile += 1
                continue

            if self.temporal_code[i] == "end if":
                if_pile -= 1
                if if_pile == 0:
                    self.ignore_index = i+1
                    self.ignore_code = True
                    if_structure = IfStructure(tmp_code, self.compiler)
                    self.execute_function = if_structure.execute_if_structure
                    return True
                
        return False
    
    def if_line(self, line: str):
        if self.ignore_if_sections == False and self.if_section_done == False:
            line = line.split()
            args = " ".join(line[1:-1])
            _if = line[0]
            _then = line[-1]
            if _if != "if" or _then != "then" or args[0] != '(' or args[-1] != ')':
                return self.compiler.error_handler(f"Error, the if structure is not well made")

            if not self.check_end_if(line):
                return self.compiler.error_handler(f"Error, the if structure doesn't have an end if statement")
        else:
            self.ifs_counter += 1

    
    def else_line(self):
        if not self.ignore_if_sections:
            self.if_section_done = True
            return
        
        if self.ifs_counter > 0:
            return

        self.ignore_if_sections = False
    
    def else_if_line(self, line: str):
        if not self.ignore_if_sections:
            self.if_section_done = True
            return
        
        if self.ifs_counter > 0:
            return

        code_line = line.split()
        code_line = " ".join(code_line[2:-1])[1:-1]
        if self.compiler.solve_equation(code_line):
            self.ignore_if_sections = False
        
    def execute_if_structure(self):
        first_line = self.temporal_code.pop(0).split()
        _if_args = " ".join(first_line[1:-1])[1:-1]

        pattern_if = r"^if\s*\(.*?\)\s*then$"
        pattern_else_if = r"^else\s+if\s*\(.*?\)\s*then$"
        pattern_else = r"^else$"

        result = self.compiler.solve_equation(_if_args)
        if result == None:
            return self.compiler.error_handler("Error, the arguments in the if structure are not well made")
        
        if result:
            self.ignore_if_sections = False

        for i, line in enumerate(self.temporal_code):
            if i == self.ignore_index:
                self.execute_function()
                self.ignore_code = False
            
            if self.compiler.compile_error_flag:
                break
            
            if not self.ignore_code:
                if line == "end if":
                    self.ifs_counter -= 1
                    continue

                # Patrón if                
                if re.fullmatch(pattern_if, line):
                    self.if_line(line)
                    continue

                # Patrón else if
                if re.fullmatch(pattern_else_if, line):
                    self.else_if_line(line)
                    continue

                # Patrón else
                if re.fullmatch(pattern_else, line):
                    self.else_line()
                    continue

                formatted_line = line.split(" ")
                main_command = formatted_line[0]

                if main_command == '':
                    continue
                
                if self.ignore_if_sections == False and self.if_section_done == False:
                    if main_command in self.compiler.reserved_words:
                        self.compiler.reserved_words[main_command](formatted_line)
                        continue

                    self.compiler.line_execution(main_command, formatted_line)
