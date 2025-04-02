import re

def get_increment(line: list[str]) -> int:
    if len(line) == 6:
        increment = line[-1]
        try:
            increment = int(increment)
        except:
            return 0
    else:
        increment = 1

    return increment

def do_line_syntax(line):
    if len(line) < 5:
        return False
    
    _do = line[0]
    operation: list[str] = (" ".join(line[1:4]))
    end = line[4]

    increment = get_increment(line)
    if increment == 0:
        return False
    
    asignation_pattern = r"^\s*([a-zA-Z_]\w*)\s*=\s*(-?\d+)\s*,\s*$"
    if _do == "do" and bool(re.match(asignation_pattern, operation)): 
        if len(line) == 6:
            end_value: str = end[:-1]
            comma: str = end[-1]
            if end_value.isnumeric() and comma == ',':
                return True

        else:
            end_value: str = end[:]
            if end_value.isnumeric():
                return True
        
    return False

def check_end_do(line: list[str], temporal_code: list[str]) -> tuple[bool, int, bool, list[str]]:
    formatted_line = " ".join(line)
    current_do_index = temporal_code.index(formatted_line)

    do_pile: int = 0

    tmp_code: list[str] = []
    pattern = "do"

    ignore_index: int = 0
    ignore_code: bool = False

    for i in range(current_do_index, len(temporal_code)):
        tmp_code.append(temporal_code[i])
        if temporal_code[i] == '':
            continue

        code_line = temporal_code[i].split()
        if code_line[0] == pattern:
            do_pile += 1
            continue

        if temporal_code[i] == "end do":
            do_pile -= 1
            if do_pile == 0:
                ignore_index = i+1
                ignore_code = True
                return True, ignore_index, ignore_code, tmp_code
            
    return False, None, None, None

def check_do_structure(line: list[str], temporal_code: list[str], compiler):
    from Tools.Structures.do_structure import DoStructure
    if not do_line_syntax(line):
        return "Error, the do structure is not well made.", None, None
    check_end_flag, ignore_index, ignore_code, tmp_code = check_end_do(line, temporal_code)
    if not check_end_flag:
        return "Error, the do structure donesn't have an end do statement", None, None
    do_structure = DoStructure(tmp_code, compiler)
    return ignore_index, ignore_code, do_structure