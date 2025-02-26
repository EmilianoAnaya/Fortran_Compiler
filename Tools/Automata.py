class Automata():
    def __init__(self):
        self.estado: str = "inicio"
        self.identificador: list = []
        self.codigo_intermedio: list = []

        self.lines: list[str] = []

        self.data_type: dict = {
           "int"    : "Entero Corto",
           "double" : "Entero Largo",
           "str"    : "String",
           "bool"   : "Boleano"
        }

    def transicion(self, caracter):
        if self.estado == "inicio":
          if caracter.isalpha() or caracter == '_':
            self.estado = "valido"
          else:
            self.estado = 'invalido'

        elif self.estado == 'valido':
          if caracter.isalnum() or caracter == '_':
            self.estado = 'valido'
          else:
            self.estado = 'invalido'

        else:
          return

    def check_validation(self, cadena: str):
        self.estado = "inicio"

        if cadena == "_":
           self.estado = 'invalido'
           return

        for caracter in cadena:
          self.transicion(caracter)
          if self.estado == 'invalido':
            return

        self.identificador.append(cadena)
        self.codigo_intermedio.append(f"IDENTIFICADOR: {cadena}")
    
    def procesar_entrada(self, input:str):
        splited_input = input.split(" ")
        for variable in splited_input:
           self.check_validation(variable)

    def check_initialization(self, lines:list[str]):
       for line in lines:
          data_type, identifier = line.split(" ")
          if data_type not in self.data_type:
             print(f"{data_type} {identifier} // no identificado")
             continue
          
          self.check_validation(identifier)
          if self.estado != "valido":
            print(f"{data_type} {identifier} // no identificado")
            continue

          print(f"{data_type} {identifier} // Tipo de dato {self.data_type[data_type]}, variable {identifier}")
             

    def set_lines(self, path_file:str):
       with open(path_file, "r") as f:
          self.lines = f.read().splitlines()

    def get_lines(self):
       return self.lines

    def get_codigo_intermedio(self):
      return self.codigo_intermedio
    
    def get_identificadores(self):
      return self.identificador