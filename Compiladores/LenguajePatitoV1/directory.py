# -----------------------------------------------------------------
# directory.py
#
# Archivo para manejar las estructuras de datos semánticas:
# - VarTable (Tabla de Variables)
# - FuncDirectory (Directorio de Funciones)
# -----------------------------------------------------------------

# --- 1. Tabla de Variables (VarTable) ---
class VarTable:
    """
    Representa una tabla de variables para un ámbito (scope) específico,
    ya sea global o local de una función.
    """
    def __init__(self):
        """
        Inicializa la tabla. El diccionario 'variables' almacenará
        la información de cada variable.
        Estructura: {'nombre_var': {'tipo': 'entero' | 'flotante', ...}}
        """
        self.variables = {}

    def add_var(self, name, type):
        """
        Añade una variable a la tabla.
        Lanza una excepción si la variable ya está declarada.
        """
        if name in self.variables:
            # Error: Variable doblemente declarada en el mismo ámbito
            raise Exception(f"Error Semántico: La variable '{name}' ya está declarada en este ámbito.")
        else:
            self.variables[name] = {'tipo': type}
            # print(f"Variable añadida a VarTable: {name} (Tipo: {type})") # Para depuración

    def lookup_var(self, name):
        """
        Busca una variable en esta tabla específica.
        Devuelve el tipo si la encuentra, o None si no.
        """
        if name in self.variables:
            return self.variables[name]['tipo']
        else:
            return None

    def __str__(self):
        """Representación en string para depuración."""
        return str(self.variables)


# --- 2. Directorio de Funciones (FuncDirectory) ---
class FuncDirectory:
    """
    Representa el directorio principal de funciones del programa.
    Contiene un diccionario de todas las funciones, incluyendo un
    ámbito 'global' especial.
    """
    def __init__(self):
        """
        Inicializa el directorio.
        Estructura: {'nombre_func': {'tipo_retorno': 'nula' | 'entero' | ...,
                                    'tabla_vars': VarTable(),
                                    'parametros': ['entero', 'flotante', ...]
                                   }
                    }
        """
        self.functions = {}
        # Pre-cargar el ámbito 'global'
        self.add_func('global', 'nula')

    def add_func(self, name, return_type):
        """
        Añade una función al directorio.
        Lanza una excepción si la función ya existe.
        """
        if name in self.functions:
            # Error: Función doblemente declarada
            raise Exception(f"Error Semántico: La función '{name}' ya está declarada.")
        else:
            self.functions[name] = {
                'tipo_retorno': return_type,
                'tabla_vars': VarTable(),
                'parametros': [] # Lista ordenada de tipos de parámetros
            }
            # print(f"Función añadida a Directorio: {name} (Tipo: {return_type})") # Para depuración
            
    def lookup_func(self, name):
        """
        Verifica si una función existe en el directorio.
        Lanza una excepción si no existe.
        """
        if name not in self.functions:
            raise Exception(f"Error Semántico: La función '{name}' no está declarada.")

    def add_var_to_func(self, func_name, var_name, var_type):
        """
        Añade una variable a la tabla de variables de una función específica.
        """
        # Primero nos aseguramos que la función exista
        self.lookup_func(func_name)
        
        # Llama al método add_var de la VarTable de esa función
        try:
            self.functions[func_name]['tabla_vars'].add_var(var_name, var_type)
        except Exception as e:
            # Re-lanza la excepción con más contexto
            raise Exception(f"Error en función '{func_name}': {e}")

    def add_param_to_func(self, func_name, param_type):
        """
        Añade el TIPO de un parámetro a la lista de parámetros de la función.
        """
        self.lookup_func(func_name)
        self.functions[func_name]['parametros'].append(param_type)

    def lookup_var_in_func(self, func_name, var_name):
        """
        Busca una variable y devuelve su tipo.
        Busca primero en el ámbito local (func_name) y, si no la
        encuentra, busca en el ámbito 'global'.
        Lanza una excepción si no la encuentra en ninguno.
        """
        # 1. Buscar en el ámbito local (la función actual)
        tipo_local = self.functions[func_name]['tabla_vars'].lookup_var(var_name)
        
        if tipo_local:
            return tipo_local
        
        # 2. Si no, buscar en el ámbito 'global'
        tipo_global = self.functions['global']['tabla_vars'].lookup_var(var_name)
        
        if tipo_global:
            return tipo_global
            
        # 3. Si no está en ningún lado, es un error
        raise Exception(f"Error Semántico: La variable '{var_name}' no está declarada.")
        
    def __str__(self):
        """Representación en string para depuración."""
        output = "--- Directorio de Funciones ---\n"
        for name, data in self.functions.items():
            output += f"Función: {name} (Retorno: {data['tipo_retorno']})\n"
            output += f"  Params: {data['parametros']}\n"
            output += f"  Vars: {str(data['tabla_vars'])}\n"
        output += "---------------------------------"
        return output