
from Tools.check_do_structure import get_increment
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Tools.automaton import Compiler

class DoStructure():
    def __init__(self, temporal_code: list[str], compiler):
        self.compiler: Compiler = compiler
        self.ignore_data: dict = {
            "code"              : temporal_code,
            "ignore_code"       : False,
            "ignore_index"      : -1,
            "execute_function"  : None
        }

        self.do_counter: int = 0
        
        self.increment_value: int = 0
        self.end_value: int = 0
        self.symbol: str = ""

    def get_symbol(self, increment:int) -> str:
        if increment > 0:
            return "<="
        else:
            return ">="
    
    def execute_select_structure(self):
        first_line = self.ignore_data["code"].pop(0).split()

        variable = first_line[1].replace("'","")
        value_for_variable = first_line[3].replace(",","")

        if not self.compiler.check_existing_variable(variable):
            return self.compiler.error_handler("Error, the variable to use in the do structure is not yet initialized")
        
        self.compiler.set_variable_value(variable, value_for_variable)
        
        self.increment_value = get_increment(first_line)
        self.symbol = self.get_symbol(self.increment_value)

        self.end_value = first_line[4].replace(",","")

        while(self.compiler.solve_equation(str(f"{self.compiler.get_variable_value(variable)} {self.symbol} {self.end_value}"))):
            for i, line in enumerate(self.ignore_data["code"]):
                if i == self.ignore_data["ignore_index"]:
                    self.ignore_data["execute_function"]()
                    self.ignore_data["ignore_code"] = False

                if i == len(self.ignore_data["code"])-1:
                    self.compiler.increment_value(variable, self.increment_value)
                    break
                
                if self.compiler.compile_error_flag:
                    break

                if not self.ignore_data["ignore_code"]:
                    formatted_line = line.split(" ")
                    main_command = formatted_line[0]

                    if main_command == '':
                        continue
                    
                    if not self.compiler.line_checker(main_command):
                        return self.compiler.error_handler(f"Error, the '{main_command}' command doesn't exists")

                    if main_command in self.compiler.control_structures:
                        self.compiler.control_structures[main_command](formatted_line, self.ignore_data)
                        continue

                    print("Error desde do")
                    self.compiler.line_execution(main_command, formatted_line)

            if self.compiler.compile_error_flag:
                break
