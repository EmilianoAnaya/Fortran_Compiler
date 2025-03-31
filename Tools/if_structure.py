import re

class IfStructure():
    def __init__(self, temporal_code: list[str], compiler):
        self.temporal_code: list[str] = temporal_code
        self.compiler: Compiler = compiler
    
    def check_end_if(self, line) -> bool:
        formatted_line = " ".join(line)
        current_if_index = self.code.index(formatted_line)
        if_pile = 0
        tmp_code: list[str] = []
        pattern = r"if\s*\(\s*[^()]+\s*\)\s*then"

        for i in range(current_if_index, len(self.code)):
            tmp_code.append(self.code[i])
            if re.fullmatch(pattern, self.code[i]):
                if_pile += 1
                continue

            if self.code[i] == "end if":
                if_pile -= 1
                if if_pile == 0:
                    print(i)
                    self.ignore_index = i
                    self.ignore_code = True
                    return True, tmp_code
                
        return False, None
    
    def execute_if_structure(self):
        
        # if_section_done: bool = False
        # ignore_if_sections: bool = False
        # 
        # tmp_code.pop(0)
        # result = self.solve_equation(args_first)
        # if result == None:
            # return self.error_handler("Error, the arguments in the if structure are not well made")
        # 
        # if result:
            # ignore_if_sections = True
# 
        # for code in tmp_code:
            # print("imprimiendo desde if_structure")
            # if self.compile_error_flag:
                # break
# 
            # formatted_line = code.split(" ")
            # main_command = formatted_line[0]
# 
            # if main_command == "":
                # continue
# 
            # if main_command in self.reserved_words:
                # self.reserved_words[main_command](formatted_line)
                # continue
            # 
            # if ignore_if_sections:
                # self.line_execution(main_command, formatted_line)