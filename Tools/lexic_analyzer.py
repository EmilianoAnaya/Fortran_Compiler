class LexicAnalyzer(): 
    def __init__(self, terminal):
        self.operands: dict = {
            "+" : "Suma",
            "-" : "Resta",
            "/" : "Divide",
            "*" : "Multiplica"
        }

        self.terminal = terminal

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
        
    def parse(self, expression):
        tmp_string: str = ""
        sub_operations: list = []
        first_operand: bool = False
        operand_appearence: bool = False

        for char in expression:
            if char.isnumeric():
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
                    self.terminal.show_line("The integrity of the operation is wrong")
                    return

        if tmp_string.isnumeric():
            sub_operations.append(tmp_string)
        
        if self.check_integrity(sub_operations):
            self.syntactic_analysis(sub_operations)
        else:
            self.terminal.show_line("The integrity of the operation is unclear")
        
        