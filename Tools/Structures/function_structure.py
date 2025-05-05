from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Tools.automaton import Compiler

class FunctionStructure():
    def __init__(self, compiler: Compiler, data_type: str, function_code: list[str], num_params: int, params: list[str]):
        self.compiler = compiler
        self.ignore_data: dict = {
            "code"              : function_code,
            "ignore_code"       : False,
            "ignore_index"      : -1,
            "execute_function"  : None
        }

        self.function_data: dict  = {
            "data_type"     : data_type,
            "num_params"    : num_params,
            "params"        : params
        }

    def execute_function(self):
        for i, line in enumerate(self.ignore_data["code"]):
            if i == self.ignore_data["ignore_index"]:
                self.ignore_data["execute_function"]()
                self.ignore_data["ignore"] = False
            
            if self.compiler.compile_error_flag:
                break

            formatted_line = line.split(" ")
            main_command = formatted_line[0]

            if main_command == '':
                continue

            if not self.ignore_data["ignore_code"]:
                print(line)