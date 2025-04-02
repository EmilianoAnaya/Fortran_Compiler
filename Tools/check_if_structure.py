import re

def if_then_else_syntax(line: list[str]) -> bool:
    args = " ".join(line[1:-1])
    _if = line[0]
    _then = line[-1]
    if _if != "if" or _then != "then" or args[0] != '(' or args[-1] != ')':
        return False
    else:
        return True

def check_end_if(line:str, temporal_code: list[str]) -> bool:
    formatted_line = " ".join(line)
    current_if_index = temporal_code.index(formatted_line)
    if_pile = 0
    tmp_code: list[str] = []
    pattern = "if"

    ignore_index: int = 0
    ignore_code: bool = False

    for i in range(current_if_index, len(temporal_code)):
        tmp_code.append(temporal_code[i])
        if temporal_code[i] == '':
            continue

        if re.fullmatch(pattern, temporal_code[i][:2]):
            if_pile += 1
            continue
        
        if temporal_code[i] == "end if":
            if_pile -= 1
            if if_pile == 0:
                ignore_index = i+1
                ignore_code = True
                return True, ignore_index, ignore_code, tmp_code
            
    return False, None, None, None

def check_if_structure(line: str, temporal_code: list[str], compiler):
    from Tools.Structures.if_structure import IfStructure
    if not if_then_else_syntax(line):
        return "Error, the if structure is not well made", None, None
    check_end_flag, ignore_index, ignore_code, tmp_code = check_end_if(line, temporal_code)
    if not check_end_flag:
        return "Error, the if structure doesn't have an end if statement", None, None
    else:
        if_structure = IfStructure(tmp_code, compiler)
        return ignore_index, ignore_code, if_structure
        
