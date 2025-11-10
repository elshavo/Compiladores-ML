# -----------------------------------------------------------------
# semantic_cube.py
#
# Implementación del Cubo Semántico como una clase.
# Contiene la lógica para validar tipos en expresiones.
# -----------------------------------------------------------------

class SemanticCube:
    def __init__(self):
        # Definimos el tipo 'booleano' internamente para comparaciones
        # y 'error' para tipos inválidos.
        self.tipos = {
            'entero': 1,
            'flotante': 2,
            'booleano': 3,
            'error': -1
        }

        # El cubo semántico real, implementado como un diccionario anidado.
        # [op_izq][op_der][operador] -> tipo_resultado
        self.cubo = {
            # entero vs ...
            self.tipos['entero']: {
                self.tipos['entero']: {
                    '+': self.tipos['entero'],
                    '-': self.tipos['entero'],
                    '*': self.tipos['entero'],
                    '/': self.tipos['entero'], # Nota: Idealmente 'flotante', pero simple 'entero'
                    '>': self.tipos['booleano'],
                    '<': self.tipos['booleano'],
                    '==': self.tipos['booleano'],
                    '!=': self.tipos['booleano'],
                    '>=': self.tipos['booleano'],
                    '<=': self.tipos['booleano'],
                    '=': self.tipos['entero'], # Asignación
                },
                self.tipos['flotante']: {
                    '+': self.tipos['flotante'],
                    '-': self.tipos['flotante'],
                    '*': self.tipos['flotante'],
                    '/': self.tipos['flotante'],
                    '>': self.tipos['booleano'],
                    '<': self.tipos['booleano'],
                    '==': self.tipos['booleano'],
                    '!=': self.tipos['booleano'],
                    '>=': self.tipos['booleano'],
                    '<=': self.tipos['booleano'],
                    '=': self.tipos['error'], # ERROR: entero = flotante (truncamiento)
                },
            },
            # flotante vs ...
            self.tipos['flotante']: {
                self.tipos['entero']: {
                    '+': self.tipos['flotante'],
                    '-': self.tipos['flotante'],
                    '*': self.tipos['flotante'],
                    '/': self.tipos['flotante'],
                    '>': self.tipos['booleano'],
                    '<': self.tipos['booleano'],
                    '==': self.tipos['booleano'],
                    '!=': self.tipos['booleano'],
                    '>=': self.tipos['booleano'],
                    '<=': self.tipos['booleano'],
                    '=': self.tipos['flotante'], # OK: flotante = entero (promoción)
                },
                self.tipos['flotante']: {
                    '+': self.tipos['flotante'],
                    '-': self.tipos['flotante'],
                    '*': self.tipos['flotante'],
                    '/': self.tipos['flotante'],
                    '>': self.tipos['booleano'],
                    '<': self.tipos['booleano'],
                    '==': self.tipos['booleano'],
                    '!=': self.tipos['booleano'],
                    '>=': self.tipos['booleano'],
                    '<=': self.tipos['booleano'],
                    '=': self.tipos['flotante'], # OK: flotante = flotante
                },
            },
        }

    def lookup(self, op_izq, op_der, operador):
        """
        Busca una operación en el cubo semántico.
        Devuelve el tipo de resultado ('entero', 'flotante', 'booleano')
        o lanza una excepción si es 'error'.
        """
        # Convertir tipos de string a nuestros IDs numéricos
        tipo_izq = self.tipos.get(op_izq, self.tipos['error'])
        tipo_der = self.tipos.get(op_der, self.tipos['error'])
        
        # Buscar en el cubo
        resultado_num = self.cubo.get(tipo_izq, {}).get(tipo_der, {}).get(operador, self.tipos['error'])
        
        if resultado_num == self.tipos['error']:
            # Error de tipos
            raise Exception(f"Error Semántico: Operación inválida. No se puede hacer '{op_izq} {operador} {op_der}'.")
        
        # Devolver el tipo de resultado como string
        for tipo_str, tipo_num in self.tipos.items():
            if tipo_num == resultado_num:
                return tipo_str
        
        return 'error' # No debería llegar aquí

# Crear una instancia global para que el parser la importe
cubo_semantico = SemanticCube()