from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Tools.automaton import Compiler

class FunctionStructure():
    def __init__(self, compiler, data_type: str, function_code: list[str], num_params: int, params: list[str], function_name: str):
        self.compiler: Compiler = compiler
        self.ignore_data: dict = {
            "code"              : function_code,
            "ignore_code"       : False,
            "ignore_index"      : -1,
            "execute_function"  : None
        }

        self.function_data: dict  = {
            "data_type"         : data_type,
            "num_params"        : num_params,
            "params"            : params,
            "return_command"    : function_name
        }

        self.received_params: list = []

        self.variables_main: dict = self.compiler.variables.copy()

    def check_params(self, params: list) -> bool:
        if len(self.function_data["params"]) == len(params):
            return True
        return False

    def parameter_initialization(self, formatted_line: list[str]):
        data_type: str = formatted_line[0]
        intent_in: str = formatted_line[1]
        
        if intent_in == "intent(in)":
            double_colon: str = formatted_line[2]
            
            if not double_colon == "::":
                return self.error_handler("Initialization Error")
            
            args: str = formatted_line[3:]
            formatted_args: list[str] = [arg.replace(",","") for arg in args]

            print(formatted_args)
            for arg in formatted_args:
                if not arg in self.compiler.variables and arg in self.function_data["params"]:
                    ...


        elif intent_in == "::":
            return self.compiler.variable_initialization(formatted_line)
        else:
            return self.error_handler("Initialization Error")
    
    def execute_function(self, params_list: list):
        self.compiler.variables = {}
        self.received_params = params_list

        for i, line in enumerate(self.ignore_data["code"]):
            if i == self.ignore_data["ignore_index"]:
                self.ignore_data["execute_function"]()
                self.ignore_data["ignore"] = False
            
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

                if main_command in self.compiler.data_type:
                    self.parameter_initialization(formatted_line)
                    continue
                
                self.compiler.line_execution(main_command, formatted_line)

        self.compiler.variables = self.variables_main.copy()