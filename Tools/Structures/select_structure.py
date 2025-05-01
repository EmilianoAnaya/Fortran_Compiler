import re
from Tools.check_select_structure import check_select_structure

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Tools.automaton import Compiler

class SelectStructure():
    def __init__(self, temporal_code: list[str], compiler):
        self.compiler: Compiler = compiler

        self.select_value_structure = None

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

        self.ignore_select_sections: bool = True
        self.select_section_done: bool = False

        self.selects_counter: int = 0

    def select_line(self, line: str):
        if self.ignore_select_sections == False and self.select_section_done == False:
            line = line.split()
            # ignore_index, ignore_code, select_structure = check_select_structure(line, self.temporal_code, self.compiler)
            ignore_index, ignore_code, select_structure = check_select_structure(line, self.ignore_data["code"], self.compiler)
            if type(ignore_index) == str:
                return self.compiler.error_handler(ignore_index)
            
            # self.ignore_index = ignore_index
            # self.ignore_code = ignore_code
            # self.execute_function = select_structure.execute_select_structure
            self.ignore_data["ignore_index"] = ignore_index
            self.ignore_data["ignore_code"] = ignore_code
            self.ignore_data["execute_function"] = select_structure.execute_select_structure
        else:
            self.selects_counter += 1
    
    def case_line(self, line: str):
        if not self.ignore_select_sections:
            self.select_section_done = True
            return
        
        if self.selects_counter > 0:
            return
        
        splitted_line = line.split()

        _case = splitted_line[0]
        args_case = splitted_line[1]

        if _case == "case":
            if args_case == "default":
                self.ignore_select_sections = False
            elif args_case[0] == "(" and args_case[-1] == ")":
                arg_value = args_case[1:-1]
                arg_value = self.compiler.clean_strings(arg_value)

                result = str(f'"{self.select_value_structure}" == "{arg_value}"')
                try:
                    expression = eval(result, {"__builtins__": None}, {})
                except TypeError:
                    return self.compiler.error_handler(f"Error, the variables used are non existing or mistakenly written in the case structure")
                
                if expression == True:
                    self.ignore_select_sections = False
            else:
                return self.compiler.error_handler(f"Error, the case statement is not well made")
    
    def execute_select_structure(self):
        # first_line = self.temporal_code.pop(0).split()
        first_line = self.ignore_data["code"].pop(0).split()
        _select_args = " ".join(first_line[2:])[1:-1]
        
        result = self.compiler.solve_equation(_select_args)
        if result == None:
            return self.compiler.error_handler("Error, the arguments in the select structure are not well made")
        else:
            result = self.compiler.clean_strings(result)
            self.select_value_structure = result

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
                if line == "end select":
                    self.selects_counter -= 1
                    continue

                formatted_line = line.split(" ")
                main_command = formatted_line[0]

                if main_command == '':
                    continue

                if main_command == "select":
                    self.select_line(line)
                    continue
                
                if main_command == "case":
                    self.case_line(line)
                    continue

                if not self.compiler.line_checker(main_command):
                    return self.compiler.error_handler(f"Error, the '{main_command}' command doesn't exists")
                
                if self.ignore_select_sections == False and self.select_section_done == False:
                    if main_command in self.compiler.control_structures:
                        self.compiler.control_structures[main_command](formatted_line, self.ignore_data)
                        continue

                    self.compiler.line_execution(main_command, formatted_line)
        
