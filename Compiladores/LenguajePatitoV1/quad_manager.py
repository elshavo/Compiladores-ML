# quad_manager.py
from semantic_cube import cubo_semantico

# --- 1. Clase para definir un Cuádruplo ---
# Usamos una clase simple para claridad
class Cuadruplo:
    def __init__(self, operador, op_izq, op_der, resultado):
        self.operador = operador
        self.op_izq = op_izq
        self.op_der = op_der
        self.resultado = resultado # Esto suele ser un temporal (t1, t2, ...)

    def __str__(self):
        # Un formato bonito para imprimir
        return f"({self.operador}, {self.op_izq}, {self.op_der}, {self.resultado})"

# --- 2. El Manejador Principal ---
class QuadManager:
    def __init__(self):
        self.fila_cuadruplos = []
        self.pila_operandos = []
        self.pila_tipos = []
        self.pila_operadores = []
        self.contador_temporales = 1 # Para t1, t2, t3...

    def generar_temporal(self):
        """Genera un nuevo nombre de variable temporal (ej. 't1')"""
        temp_nombre = f"t{self.contador_temporales}"
        self.contador_temporales += 1
        return temp_nombre

    def agregar_cuadruplo(self, operador, op_izq, op_der, resultado):
        """Crea y añade un nuevo cuádruplo a la fila"""
        nuevo_quad = Cuadruplo(operador, op_izq, op_der, resultado)
        self.fila_cuadruplos.append(nuevo_quad)
        # print(f"Cuádruplo Generado: {nuevo_quad}") # Para depuración

    def mostrar_cuadruplos(self):
        """Imprime la fila completa de cuádruplos al final"""
        print("\n--- Fila de Cuádruplos ---")
        for i, quad in enumerate(self.fila_cuadruplos):
            print(f"{i}: {quad}")
        print("--------------------------")

    # --- Métodos para Pilas ---
    
    def push_operando_tipo(self, operando, tipo):
        """Mete un operando y su tipo a las pilas"""
        self.pila_operandos.append(operando)
        self.pila_tipos.append(tipo)

    def push_operador(self, operador):
        """Mete un operador a la pila"""
        self.pila_operadores.append(operador)

    # --- Métodos de Puntos Neurálgicos (los llamaremos desde el parser) ---
    
    def generar_cuadruplo_expresion(self):
        """
        Punto Neurálgico para `exp` (Sumas/Restas) y `termino` (Mult/Div).
        Saca los 2 operandos y 1 operador de la cima para generar
        un cuádruplo.
        """
        # 1. Sacar operandos y tipos
        op_der = self.pila_operandos.pop()
        op_izq = self.pila_operandos.pop()
        tipo_der = self.pila_tipos.pop()
        tipo_izq = self.pila_tipos.pop()
        
        # 2. Sacar operador
        operador = self.pila_operadores.pop()
        
        # 3. Validar con Cubo Semántico
        tipo_resultado = cubo_semantico.lookup(tipo_izq, tipo_der, operador)
        
        # 4. Generar el temporal y el cuádruplo
        temporal = self.generar_temporal()
        self.agregar_cuadruplo(operador, op_izq, op_der, temporal)
        
        # 5. Meter el resultado de vuelta a las pilas
        self.push_operando_tipo(temporal, tipo_resultado)

# --- Instancia global que el parser importará ---
quad_manager = QuadManager()