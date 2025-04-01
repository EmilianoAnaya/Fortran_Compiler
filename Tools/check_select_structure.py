
def select_line_syntax(line: list[str]) -> bool:
    _select = line[0]
    _case = line[1]
    args = line[2:]
    args = " ".join(args)
    if _select != "select" or _case != "case" or args[0] != '(' or args[-1] != ')':
        return False
    else: 
        return True

def check_end_select(line: list[str], temporal_code: list[str]) -> bool:
    formatted_line = " ".join(line)
    current_select_index = temporal_code.index(formatted_line)

    select_pile = 0

    tmp_code: list[str] = []
    pattern = "select"

    ignore_index: int = 0
    ignore_code: bool = False

    for i in range(current_select_index, len(temporal_code)):
        tmp_code.append(temporal_code[i])
        code_line = temporal_code[i].split()
        if temporal_code[i] == '':
            continue

        if code_line[0] == pattern:
            select_pile += 1
            continue
        if temporal_code[i] == "end select":
            select_pile -= 1
            if select_pile == 0:
                ignore_index = i+1
                ignore_code = True
                return True, ignore_index, ignore_code, tmp_code
    
    return False, None, None, None

def check_select_structure(line: list[str], temporal_code: list[str], compiler):
    from Tools.Structures.select_structure import SelectStructure
    if not select_line_syntax(line):
        return "Error, the select structure is not well made", None, None
    check_end_flag, ignore_index, ignore_code, tmp_code = check_end_select(line, temporal_code)
    if not check_end_flag:
        return "Error, the select structure doesn't have an end select statement", None, None
    else:
        select_structure = SelectStructure(tmp_code, compiler)
        return ignore_index, ignore_code, select_structure