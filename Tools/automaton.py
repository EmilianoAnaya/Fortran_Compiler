import re
import ast
import json
from constants import Routes
from typing import TYPE_CHECKING
from Tools.Structures.function_structure import FunctionStructure
from Tools.check_if_structure import check_if_structure
from Tools.check_select_structure import check_select_structure
from Tools.check_do_structure import check_do_structure
# from Tools.select_structure import SelectStructure

if TYPE_CHECKING:
    from Components.terminal_frame import TerminalFrame

class Compiler():
    def __init__(self, terminal, Testing=False):
        self.data_type: dict = {
            "integer" : int,
            "real" : float,
            "complex" : complex,
            "character" : str,
            "logical" : bool
        }

        self.array_regex_type: dict = {
            "integer" : r'^\[\s*(-?\d+\s*(,\s*-?\d+\s*)*)?\]$',
            "real" : r'^\[\s*(-?\d+\.\d+\s*(,\s*-?\d+\.\d+\s*)*)?\]$',
            "character" : r'^\[\s*(".*?"\s*(,\s*".*?"\s*)*)?\]$',
            "logical" : r'^\[\s*(true|false)\s*(,\s*(true|false)\s*)*\]$'
        }

        self.operands: dict = {
            "+" : "Suma",
            "-" : "Resta",
            "*" : "Multiplica",
            "/" : "Divide",
            "=" : "Iguala",
            ">" : "Mayor",
            "<" : "Menor",
            ">=": "Mayor o igual",
            "<=": "Menor o igual",
            "==": "Igual que"
        }

        self.commands : dict = {
            "print*," : self.print_args
        }

        self.control_structures : dict = {
            "if"    : self.validation_structure,
            "select": self.select_command,
            "do"    : self.do_structure
        }
        
        self.reserved_words : dict = {
            "use"   : self.add_libraries,
            "end"   : self.end_command,
        }

        self.words_for_structures: list = [
            "case",
            "else"
        ]
        
        # Debug Tools
        self.testing_flag = Testing
        # 

        self.terminal:TerminalFrame = terminal
        self.compile_error_flag: bool = False
        
        self.ignore_data: dict = {
            "code"              : None,
            "ignore_code"       : False,
            "ignore_index"      : -1,
            "execute_function"  : None
        }
        
        self.code: list[str] = None
        self.ignore_code: bool = False
        self.ignore_index: int = -1
        self.execute_function: function = None

        self.current_libraries: dict = {}
        self.variables: dict = {}
        self.functions: dict = {}
    
    # Debug Functions #
    def showing_messages(self, msg):
        if self.testing_flag:
            print(msg)
        else:
            self.terminal.show_line(msg)
    ####################
    def reset_all(self):
        self.ignore_data: dict = {
            "code"              : None,
            "ignore_code"       : False,
            "ignore_index"      : -1,
            "execute_function"  : None
        }
        self.compile_error_flag: bool = False
        self.current_libraries: dict = {}
        self.variables: dict = {}

    # def check_for_arrays(self, equation: str) -> str:
    #     ...

    def get_function_params(self, equation: str, function_name: str):
        initial_bracket: int = equation.find("[")
        bracket_pile: int = 0
        
        params_string: str = ""
        
        for index in range(initial_bracket, len(equation)):
            char: str = equation[index]
            params_string = params_string + char

            if char == '[':
                bracket_pile += 1

            if char == ']':
                bracket_pile -= 1

            if bracket_pile == 0:
                break
        
        if bracket_pile != 0:
            return None
        
        return params_string
    
    def find_functions(self, equation: str) -> tuple:
        for function in self.functions:
            while True:
                index_function: int = equation.find(f"{function}[")

                if index_function == -1:
                    break
                
                params = self.get_function_params(equation, function)
                if params == None:
                    return True, None

                params_list: list = self.solve_equation(params)
                if params_list == None:
                    return True, None

                if not self.functions[function].check_params(params_list):
                    return True, None

                result = self.functions[function].execute_function(params_list)

                if self.compile_error_flag:
                    return True, None

                function_part = f"{function}{params}"
                equation = equation.replace(function_part, str(result))

        # print(equation)
        return False, equation
            # while True:
                # index_function = equation.find(function)
# 
                # if index_function == -1:
                    # break

    
    def solve_equation(self, equation: str, msg=None):
        if msg != None:
            print(msg)
        parsed_variables = {key: value["value"] for key, value in self.variables.items()}

        equation = str(equation)
        equation = equation.replace("(","[").replace(")","]")
        
        # self.find_functions(equation)
        error_flag, formatted_equation = self.find_functions(equation)
        if self.compile_error_flag:
            return None
        
        if error_flag:
            self.showing_messages("Error, a function was found but it syntax is wrong")
            return None

        try:
            return eval(formatted_equation, {"__builtins__": None}, parsed_variables)
        except TypeError:
            self.showing_messages("The data type of the expressions used are different from each other")
        except SyntaxError:
            self.showing_messages(f"The syntaxis of the expression '{equation}' is wrongly used")
        except IndexError:
            self.showing_messages(f"Error, it was tried to access to an index which the array doesn't have")
        return None
    
    def clean_strings(self, string: str) -> str:
        if type(string) == str:
            string = string[1:-1] if string[0] == '"' and string[-1] == '"' else string
        return string
    
    def check_existing_variable(self, variable):
        if variable in self.variables:
            return True
        return False
    
    def increment_value(self, variable: str, increment: int) -> None:
        self.variables[variable]["value"] = self.solve_equation(f"{self.variables[variable]["value"]} + {increment}")
    
    def set_variable_value(self, variable, value):
        self.variables[variable]["value"] = int(value)
    
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
        self.showing_messages(f"{identation}{self.operands[operand]}: {operand}")
        if type(tree[0]) == list:
            self.syntactic_analysis(tree[0], level+1)
        else:
            self.showing_messages(f"{identation} Numero: {tree[0]}")
        self.showing_messages(f"{identation} Numero: {tree[2]}")
        
    def error_handler(self, msg):
        self.compile_error_flag = True
        self.showing_messages(msg)
    
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

            if self.is_array(arg):
                if self.check_array_syntax(arg):
                    array_index, array_name = self.tokenize_array(arg)
                    output.append(self.get_array_data(array_name, array_index))
                    continue
            
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
        
        self.showing_messages(" ".join(map(str, output)))

    def end_command(self, line):
        reserved_word = line[1]
        args = line[2:]
        if not reserved_word in self.reserved_words:
            return self.error_handler(f"Error, the argument {reserved_word}")
        
        if reserved_word == "if":
            self.end_if_flag = False
            self.if_section_done = False
            self.ignore_if_sections = False
            return
        
        if reserved_word == "select":
            self.end_select_flag = False
            self.select_section_done = False
            self.ignore_select_sections = False
            return
        
    def do_structure(self, line, ignore_data):
        ignore_index, ignore_code, do_structure = check_do_structure(line, ignore_data["code"], self)
        if (type(ignore_index)) == str:
            return self.error_handler(ignore_index)

        ignore_data["ignore_index"] = ignore_index
        ignore_data["ignore_code"] = ignore_code
        ignore_data["execute_function"] = do_structure.execute_do_structure
    
    def select_command(self, line, ignore_data):
        # ignore_index, ignore_code, select_structure = check_select_structure(line, self.code, self)
        ignore_index, ignore_code, select_structure = check_select_structure(line, ignore_data["code"], self)
        if (type(ignore_index)) == str:
            return self.error_handler(ignore_index)

        # self.ignore_index = ignore_index
        # self.ignore_code = ignore_code
        # self.execute_function = select_structure.execute_select_structure
        ignore_data["ignore_index"] = ignore_index
        ignore_data["ignore_code"] = ignore_code
        ignore_data["execute_function"] = select_structure.execute_select_structure

    def validation_structure(self, line, ignore_data):
        # ignore_index, ignore_code, if_structure = check_if_structure(line, self.code, self)
        ignore_index, ignore_code, if_structure = check_if_structure(line, ignore_data["code"], self)
        if type(ignore_index) == str:
            return self.error_handler(ignore_index)
        
        # self.ignore_index = ignore_index
        # self.ignore_code = ignore_code
        # self.execute_function = if_structure.execute_if_structure
        ignore_data["ignore_index"] = ignore_index
        ignore_data["ignore_code"] = ignore_code
        ignore_data["execute_function"] = if_structure.execute_if_structure

    def formating_operation(self, args):
        for i, arg in enumerate(args):
                if arg in self.variables:
                    if self.variables[arg]["value"] == None:
                        return self.error_handler(f"The {arg} variable has not yet a value"), False
                    args.pop(i)
                    args.insert(i, str(self.variables[arg]["value"]))
            
        operation = " ".join(args)
        return operation
    
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
                    return self.showing_messages("The integrity of the operation is wrong")
                    
        if tmp_string.isalnum():
            sub_operations.append(tmp_string)
        
        if not self.check_integrity(sub_operations):
            return self.error_handler("The integrity of the operation is unclear"), False

        if args != None:
            operation = self.formating_operation(args)
            return operation, True

    def variable_initialization(self, line):
        data_type = line[0]
        double_colon = line[1]
        
        if not double_colon == "::":
            return self.error_handler("Initialization Error")
        
        args: str = line[2:]
        formatted_args: list[str] = [arg.replace(",","") for arg in args]

        for arg in formatted_args:
            if not arg in self.variables:
                arg_index = arg.find("(")
                if arg_index != -1:
                    if not arg[-1] == ")":
                        return self.error_handler(f"Error, the array is not initialized correctly")
                    variable_name: str = arg[:arg_index]
                    size: str = arg[arg_index+1:-1]

                    if size == 0 or not size.isdecimal():
                        return self.error_handler(f"Error, the array '{variable_name}' is initialized incorrectly")
        
                    self.variables[variable_name] = {"data_type" : data_type, "value" : [None]*int(size), "size" : int(size), "is_list" : True}
                else:
                    self.variables[arg] = {"data_type" : data_type, "value" : None, "size" : 1, "is_list" : False}
            else:
                return self.error_handler(f"The {arg} variable has been initialized before as a {self.variables[arg]["data_type"]}")
    
    def is_math_operation(self, expression):
        operator_detected = False
        for char in expression:
            if char in self.operands:
                operator_detected = True
        return operator_detected
    
    def is_array(self, main_variable: str) -> bool:
        variable: str = main_variable
        bracket_position: int = main_variable.find("(")
        if bracket_position != -1:
            variable = variable[:bracket_position]

        if variable in self.variables and self.variables[variable]['is_list'] == True:
            return True
        
        return False
    
    def is_integer(self, variable_name: str) -> bool:
        if self.variables[variable_name]["data_type"] == "integer":
            return True
        return False
    
    def is_variable(self, array_index: str) -> str:
        if array_index.isdecimal():
            return array_index
        if array_index in self.variables:
            if self.is_integer(array_index):
                return str(self.variables[array_index]["value"])
        return str(-1)

    def check_array_syntax(self, array: str) -> bool:
        bracket_position: int = array.find("(")
        if bracket_position != -1: 
            if array[-1] == ")":
                variable_name = array[:bracket_position]
                array_index = array[bracket_position+1:-1]
                array_index = self.is_variable(array_index)
                if array_index.isdecimal():
                    if (int(array_index) <= self.variables[variable_name]['size']-1 and
                        int(array_index) >= 0):
                        return True
        else:
            if not array[-1] == ")":
                return True
        return False

    def set_array_data(self, array_index: int, array_name: str, expression: str):
        array_data_type = self.variables[array_name]["data_type"]
        if array_index != -1:
            try:
                self.variables[array_name]["value"][array_index] = self.data_type[array_data_type](expression)
            except ValueError:
                return self.error_handler(f"Error, the data type for {expression} array it's different from the array itself")
            except TypeError:
                return self.error_handler(f"Error, it was tried to set a list in a position when the argument must be a string, a bytes-like object or a real number, not 'list' ")

        else:
            pattern = self.array_regex_type[array_data_type]
            try:
                expression = str(self.solve_equation(expression))
                if re.match(pattern, expression):
                    expression_list = ast.literal_eval(expression)
                    if len(expression_list) != self.variables[array_name]["size"]:
                        return self.error_handler("The array you are trying to save it's not the same size as the stipulated in the variable")
                    self.variables[array_name]["value"] = expression_list
                else:
                    self.error_handler("The syntax of the array you're trying to save is incorrect and/or the data type of the elements it's different from the array")
            except TypeError:
                self.error_handler(f"Error, you're trying to save an element to the whole array '{array_name}' instead of one space in it")
    
    def get_array_data(self, array_name: str, array_index: int = -1):
        if array_index != -1:
            return self.variables[array_name]["value"][array_index]
        array_value = self.variables[array_name]["value"]
        array_value = " ".join(str(value) for value in array_value)
        return array_value
    
    def tokenize_array(self, array: str) -> tuple[int, str]:
        bracket_position: int = array.find("(")
        if bracket_position != -1:
            array_index = array[bracket_position+1:-1]
            array_index = int(self.is_variable(array_index))
            variable_name: str = array[:bracket_position]
        else:
            array_index: int = -1
            variable_name: str = array

        return array_index, variable_name
    
    def check_operation(self, line):
        main_variable = line[0]
        operation = line[1]
        args = line[2:]
        if operation == "=":
            expression = " ".join(args)

            expression = self.solve_equation(expression)
            if expression == None:
                return self.error_handler("The integrity of the operation is unclear")
            
            # if self.is_math_operation(expression):
            #   expression = self.solve_equation(expression)
            #     if expression == None:
            #         return self.error_handler("The integrity of the operation is unclear")
                # result, flag = self.parse(expression, args)
                # if not flag:
                    # return

            # Validar si la expresion no es Boleana.
            if expression not in ("False", "True"):
                if self.is_array(main_variable):
                    if self.check_array_syntax(main_variable):
                        array_index, array_name = self.tokenize_array(main_variable)
                        self.set_array_data(array_index, array_name, expression)
                    else:
                        return self.error_handler("Error, the syntaxis of the array is not well made")
                else:
                    try: 
                        self.variables[main_variable]["value"] = self.data_type[self.variables[main_variable]["data_type"]](expression)
                    except ValueError:
                        return self.error_handler(f"Error, the data type for {main_variable} value it's different for the variable itself")
            else:
                self.variables[main_variable]["value"] = expression.capitalize()
        # else:
        #     result = self.formating_operation(line)
        #     try:
        #         expression = eval(result, {"__builtins__": None}, {})
        #     except SyntaxError:
        #         return self.error_handler(f"Error, the arguments for the if structure are not well made")
        #     except TypeError:
        #         return self.error_handler(f"Error, the variables used are non existing or mistakenly written in the if-then-else structure")
        #     if expression:
        #         self.ignore_if_sections = False           
    
    def line_checker(self, main_command: str) -> bool:
        if (main_command in self.commands or 
            main_command in self.data_type or 
            main_command in self.variables or 
            main_command in self.control_structures or 
            main_command in self.reserved_words or
            main_command in self.words_for_structures or
            self.is_array(main_command)):
            return True
        else:
            return False
    
    
    def line_execution(self, main_command: str, formatted_line: str) -> None:  
        if main_command in self.reserved_words:
            self.reserved_words[main_command](formatted_line)
            return
        
        if main_command in self.commands:
            self.commands[main_command](formatted_line)
            return
        
        if main_command in self.data_type:
            self.variable_initialization(formatted_line)
            return
        
        if main_command in self.variables or self.is_array(main_command):
            self.check_operation(formatted_line)
            return
        
        return self.error_handler(f"Error, '{main_command}' command used is non existing")       
    
    def check_program_line(self, line: str, program_name: str) -> bool:
        tokenized_line = line.split()
        if len(tokenized_line) != 2:
            return False
        
        line_program = tokenized_line[0]
        line_name = tokenized_line[1]

        if line_program != "program" or line_name != program_name:
            return False
        
        return True
    
    def get_main_program(self, code: list[str], program_name: str) -> list[str]:
        end_line: str = f"end program {program_name}"
        if not end_line in code:
            return None
        
        main_code: list[str] = []
        end_line_index: int = code.index(end_line)
        for _ in range(end_line_index):
            main_code.append(code.pop(0))
        
        code.remove(end_line)

        return main_code

    def count_num_params(self, params: str) -> int:
        formatted_params = params[1:-1].strip()
        
        if not formatted_params:
            return 0
        
        elements = [e.strip() for e in formatted_params.split(',')]

        return len(elements)
    
    def check_function_syntaxis(self, tokenized_line: list[str]) -> tuple:
        function_word: str = tokenized_line[1]
        function_name_params: str = " ".join(tokenized_line[2:])

        params_pattern = r'^\(\s*(\w+(, \w+)*)?\s*\)$'
        name_pattern = r'^[a-zA-Z_]\w*$'

        if function_name_params[-1] != ")":
            return False, None, None, None
        
        try:
            function_name, function_params = function_name_params.split("(")
            function_params = "(" + function_params

            if function_word != "function" or not re.match(name_pattern, function_name) or not re.match(params_pattern, function_params):
                return False, None, None, None
            
            num_params: int = self.count_num_params(function_params)

            function_params = function_params.replace("(","").replace(")","").replace(",","")
            function_params = function_params.split(" ")
            
            return True, function_name, num_params, function_params
        
        except ValueError:
            return False, None, None, None
    
    def save_functions_data(self, lines: list[str], start_index: int, function_name: str, num_params: int, data_type: str, params: list) -> bool:
        stop_line: str = f"end function {function_name}"
        code_function: list[str] = []

        end_line_found: bool = False
        for i in range(start_index+1, len(lines)):
            line: str = lines[i]

            if line == '':
                continue

            if line != stop_line:
                code_function.append(line)
                continue
            
            end_line_found = True
            break
        
        if not end_line_found:
            return False
        
        last_line: list[str] = code_function[-1].split()
        return_name: str = last_line[0]

        if return_name != function_name or last_line[1] != "=":
            return False
        
        self.functions[function_name] = FunctionStructure(
            self, data_type, code_function, num_params, params, function_name
        )
        
        # self.functions[function_name] = {
            # "code" : code_function,
            # "data_type"     : data_type,
            # "num_params"    : num_params,
            # "params"        : params
        # }
        return True

    def check_functions(self, lines: list[str]) -> bool: 
        for index, line in enumerate(lines):
            if line == "":
                continue

            tokenized_line: list[str] = line.split()
            function_data_type: str = tokenized_line[0]

            if function_data_type in self.data_type:
                error_flag, function_name, num_params, params = self.check_function_syntaxis(tokenized_line)
                if not error_flag:
                    continue
                
                if not self.save_functions_data(lines, index, function_name, num_params, function_data_type, params):
                    return True

        return False

    def compile(self, lines: list[str], program_name: str):
        if not self.check_program_line(lines.pop(0), program_name):
            return self.error_handler("Error, the code has an incorrect name in the program line or the line has an incorrect syntaxis")
        
        main_code = self.get_main_program(lines, program_name)
        if main_code == None:
            return self.error_handler("Error when starting the program. The Code doesn't have an 'end program' line or its syntax is wrong.")
        
        self.ignore_data["code"] = main_code
        if self.check_functions(lines):
            return self.error_handler("Error when checking for functions. It appears a function is not well made, try checking all the structure for any syntaxis problems.")

        for i, line in enumerate(main_code):
            # if i == self.ignore_index:
            if i == self.ignore_data["ignore_index"]:
                # self.execute_function()
                self.ignore_data["execute_function"]()
                # self.ignore_code = False
                self.ignore_data["ignore_code"] = False

            if self.compile_error_flag:
                break

            formatted_line = line.split(" ")
            main_command = formatted_line[0]

            if main_command == '':
                continue
            
            # if self.ignore_code == False:
            if self.ignore_data["ignore_code"] == False:
                if main_command in self.control_structures:
                    self.control_structures[main_command](formatted_line, self.ignore_data)
                    continue

                self.line_execution(main_command, formatted_line)
