import json
from typing import TYPE_CHECKING
from constants import Routes

if TYPE_CHECKING:
    from Components.terminal_frame import TerminalFrame

class Compiler():
    def __init__(self, terminal):
        self.data_type: dict = {
            "integer" : int,
            "real" : float,
            "complex" : complex,
            "character" : str,
            "logical" : bool
        }

        self.operands: dict = {
            "+" : "Suma",
            "-" : "Resta",
            "*" : "Multiplica",
            "/" : "Divide",
            "=" : "Iguala"
        }

        self.commands : dict = {
            "print*," : self.print_args,
            "use" : self.add_libraries
        }

        self.terminal:TerminalFrame = terminal
        self.compile_error_flag: bool = False
        self.current_libraries: dict = {}
        self.variables: dict = {}
    
    def get_variable_value(self, variable):
        return self.variables[variable]["value"]
    
    def check_integrity(self, branch: list) -> bool:
        if len(branch) == 3:
            if type(branch[0]) == list:
                flag = self.check_integrity(branch[0])
                return flag
            else:
                return True
        else:
            return False

    def syntactic_analysis(self, tree: list, level: int = 0):
        identation: str = " "*level
        operand: str = tree[1]
        self.terminal.show_line(f"{identation}{self.operands[operand]}: {operand}")
        if type(tree[0]) == list:
            self.syntactic_analysis(tree[0], level+1)
        else:
            self.terminal.show_line(f"{identation} Numero: {tree[0]}")
        self.terminal.show_line(f"{identation} Numero: {tree[2]}")
        
    def error_handler(self, msg):
        self.compile_error_flag = True
        self.terminal.show_line(msg)
    
    def add_libraries(self, line: list[str]):
        main_library = line[1].replace(",","")
        if len(line) >= 5:
            only = line[2]
            colon = line[3]
            libraries: list[str] = line[4:]

            if only != "only" or colon != ":":
                return self.error_handler("Error with the sintaxis of the inclusion of libraries")
            
            with open(Routes.LIBRARIES.value, "r", encoding="utf-8") as file:
                data = json.load(file)
                for library in libraries:
                    library = library.replace(",","")
                    try:
                        self.current_libraries[library] = data[main_library][library] 
                    except KeyError:
                        return self.error_handler(f"Error, The library {library} does not exists")
                                      
        elif len(line) == 2:
            with open(Routes.LIBRARIES.value, "r", encoding="utf-8") as file:
                data = json.load(file)
                try:
                    self.current_libraries[main_library] = data[main_library]
                except KeyError:
                    return self.error_handler(f"Error, The library {library} does not exists")
                    
        else:
            return self.error_handler("Error with the sintaxis of the inclusion of libraries")
    
    def print_args(self, line):
        args: list[str] = line[1:]
        tmp_string: str = ""
        open_string: bool = False
        output: list[str] = []
        for arg in args:
            arg = arg.replace(",","")
            
            if arg in self.variables:
                output.append(self.get_variable_value(arg))
                continue

            if arg.startswith('"') and arg.endswith('"'):
                output.append(arg[1:-1])
                continue
            
            if arg.startswith('"'):
                tmp_string = arg[1:]
                open_string = True
                continue

            if arg.endswith('"'):
                tmp_string += " " + arg[:-1]
                output.append(tmp_string)
                tmp_string = ""
                open_string = False
                continue
            
            if open_string:
                tmp_string += " " + arg
                continue

            return self.error_handler(f"Error, the {arg} value is not defined")
        
        self.terminal.show_line(" ".join(map(str, output)))
    
    def parse(self, expression, args: list = None):
        tmp_string: str = ""
        sub_operations: list = []
        first_operand: bool = False
        operand_appearence: bool = False

        for char in expression:
            if char.isalnum() or char == ".":
                operand_appearence = True
                tmp_string = tmp_string + char
                continue

            if char in self.operands:
                if operand_appearence:
                    operand_appearence = False
                    sub_operations.append(tmp_string)
                    if first_operand:
                        sub_operations = [sub_operations]
                    else:        
                        first_operand = True
                    sub_operations.append(char)
                    tmp_string = ""
                else:
                    return self.terminal.show_line("The integrity of the operation is wrong")
                    

        if tmp_string.isalnum():
            sub_operations.append(tmp_string)
        
        if not self.check_integrity(sub_operations):
            return self.error_handler("The integrity of the operation is unclear"), False

        if args != None:
            for i, arg in enumerate(args):
                if arg in self.variables:
                    if self.variables[arg]["value"] == None:
                        return self.error_handler(f"The {arg} variable has not yet a value"), False
                    args.pop(i)
                    args.insert(i, str(self.variables[arg]["value"]))
            
            operation = " ".join(args)
            return operation, True

    def variable_initialization(self, line):
        data_type = line[0]
        double_colon = line[1]
        
        if not double_colon == "::":
            return self.error_handler("Initialization Error")
        
        args = line[2:]
        formatted_args = [arg.replace(",","") for arg in args]

        for arg in formatted_args:
            if not arg in self.variables:
                self.variables[arg] = {"data_type" : data_type, "value" : None}
            else:
                return self.error_handler(f"The {arg} variable has been initialized before has a {self.variables[arg]["data_type"]}")
    
    def is_math_operation(self, expression):
        operator_detected = False
        for char in expression:
            if char in self.operands:
                operator_detected = True
        return operator_detected
    
    def check_operation(self, line):
        main_variable = line[0]
        operation = line[1]
        args = line[2:]
        if operation == "=":
            expression = " ".join(args)
            if self.is_math_operation(expression):
                result, flag = self.parse(expression, args)
                if not flag:
                    return
                expression = eval(result, {"__builtins__": None}, {})
            if expression not in ("False", "True"):
                try: 
                    self.variables[main_variable]["value"] = self.data_type[self.variables[main_variable]["data_type"]](expression)
                except ValueError:
                    return self.error_handler(f"Error, the data type for {main_variable} value it's different for the variable itself")
            else:
                self.variables[main_variable]["value"] = expression.capitalize()

    def reset_all(self):
        self.compile_error_flag: bool = False
        self.current_libraries: dict = {}
        self.variables: dict = {}             
    
    def compile(self, lines: list[str]):
        self.reset_all()
        self.compile_error_flag = False
        for line in lines:
            if self.compile_error_flag:
                break
            formated_line = line.split(" ")
            main_command = formated_line[0]

            if main_command in self.data_type:
                self.variable_initialization(formated_line)
                continue

            if main_command in self.variables:
                self.check_operation(formated_line)
                continue

            if main_command in self.commands:
                self.commands[main_command](formated_line)
                continue

            return self.terminal.show_line(f"Error, '{main_command}' command used is non existing")