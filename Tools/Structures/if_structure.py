import re
from Tools.check_if_structure import check_if_structure, if_then_else_syntax

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Tools.automaton import Compiler

class IfStructure():
    def __init__(self, temporal_code: list[str], compiler):
        self.compiler: Compiler = compiler
        
        self.ignore_data: dict = {
            "code"              : temporal_code,
            "ignore_code"       : False,
            "ignore_index"      : -1,
            "execute_function"  : None
        }
        
        # self.temporal_code: list[str] = temporal_code
        # self.ignore_code: bool = False
        # self.ignore_index: int = -1
        # self.execute_function: function = None
        
        self.ignore_if_sections: bool = True
        self.if_section_done: bool = False

        self.ifs_counter: int = 0
    
    def if_line(self, line: str):
        if self.ignore_if_sections == False and self.if_section_done == False:
            line = line.split()
            # ignore_index, ignore_code, if_structure = check_if_structure(line, self.temporal_code, self.compiler)
            ignore_index, ignore_code, if_structure = check_if_structure(line, self.ignore_data["code"], self.compiler)
            if type(ignore_index) == str:
                return self.compiler.error_handler(ignore_index)

            # self.ignore_index = ignore_index
            # self.ignore_code = ignore_code
            # self.execute_function = if_structure.execute_if_structure
            self.ignore_data["ignore_code"] = ignore_code
            self.ignore_data["ignore_index"] = ignore_index
            self.ignore_data["execute_function"] = if_structure.execute_if_structure
            
        else:
            self.ifs_counter += 1

    
    def check_else_line(self, line:str):
        if not self.ignore_if_sections:
            self.if_section_done = True
            return
        
        if self.ifs_counter > 0:
            return
        
        if len(line) > 1:
            if_line = line[1:]
            if if_then_else_syntax(if_line):
                code_line = " ".join(line[2:-1])[1:-1]
                if self.compiler.solve_equation(code_line):
                    self.ignore_if_sections = False
            else:
                return self.compiler.error_handler("Error, the arguments for the if structure are not well made.")
        else:
            self.ignore_if_sections = False
        
    def execute_if_structure(self):
        # first_line = self.temporal_code.pop(0).split()
        first_line = self.ignore_data["code"].pop(0).split()
        _if_args = " ".join(first_line[1:-1])[1:-1]

        result = self.compiler.solve_equation(_if_args)
        if result == None:
            return self.compiler.error_handler("Error, the arguments in the if structure are not well made")
        
        if result:
            self.ignore_if_sections = False

        # for i, line in enumerate(self.temporal_code):
        for i, line in enumerate(self.ignore_data["code"]):
            # if i == self.ignore_index:
            if i == self.ignore_data["ignore_index"]:
                # self.execute_function()
                self.ignore_data["execute_function"]()
                # self.ignore_code = False
                self.ignore_data["ignore_code"] = False
            
            if self.compiler.compile_error_flag:
                break
            
            # if not self.ignore_code:
            if not self.ignore_data["ignore_code"]:
                if line == "end if":
                    self.ifs_counter -= 1
                    continue
                
                formatted_line = line.split(" ")
                main_command = formatted_line[0]

                if main_command == '':
                    continue

                if main_command == "if":
                    self.if_line(line)
                    continue
                
                if main_command == "else":
                    self.check_else_line(formatted_line)
                    continue
                
                if not self.compiler.line_checker(main_command):
                    return self.compiler.error_handler(f"Error, the '{main_command}' command doesn't exists")
                
                if self.ignore_if_sections == False and self.if_section_done == False:
                    if main_command in self.compiler.control_structures:
                        self.compiler.control_structures[main_command](formatted_line, self.ignore_data)
                        continue

                    self.compiler.line_execution(main_command, formatted_line)
