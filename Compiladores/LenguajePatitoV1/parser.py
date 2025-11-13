# -----------------------------------------------------------
# parser.py
#
# ETAPA 3 (Generación de Cuádruplos)
# - Se integra el 'quad_manager' para manejar pilas y la fila de cuádruplos.
# - Se eliminó la lógica de Etapa 2 (p[0] = tipo) de las expresiones.
# - Se añadieron Puntos Neurálgicos (PN) para generar cuádruplos
#   de expresiones y estatutos lineales (asigna, imprime).
# -----------------------------------------------------------

import ply.yacc as yacc
import sys

# --- 1. NUEVOS IMPORTS Y GLOBALES DE SEMÁNTICA ---

# Importa TODO de lexer.py (tokens)
from lexer import *
# Importamos nuestras clases de semántica
from directory import FuncDirectory
from semantic_cube import cubo_semantico
# ===== ¡NUEVO IMPORT! =====
from quad_manager import quad_manager # Importamos nuestro manejador

# --- Instancias Globales para Semántica ---
dir_general = FuncDirectory() # Nuestra instancia principal del Directorio
ambito_actual = 'global'      # Para saber en qué función estamos

# -----------------------------------------------------------
# 2. PRECEDENCIA DE OPERADORES (Sin cambios)
# -----------------------------------------------------------
precedence = (
    ('left', 'MAYOR', 'MENOR', 'DIF', 'IGUALDAD', 'MAYORIG', 'MENORIG'), # Nivel 4
    ('left', 'MAS', 'MENOS'),                                         # Nivel 3
    ('left', 'POR', 'DIV'),                                           # Nivel 2
    ('right', 'UMAS', 'UMENOS')                                       # Nivel 1
)

# -----------------------------------------------------------
# 3. DEFINICIÓN DE LA GRAMÁTICA (CON PUNTOS NEURÁLGICOS)
# -----------------------------------------------------------

# --- <Programa> (Sin cambios) ---
start = 'programa'

def p_programa(p):
    'programa : PROGRAMA ID pn_programa_inicio PTOCOMA vars_opcional funcs_opcional INICIO cuerpo FIN'
    print("¡Sintaxis de 'programa' correcta!")
    
    # La impresión del directorio y cuádruplos se hace en __main__
    pass

def p_pn_programa_inicio(p):
    'pn_programa_inicio :'
    # El ámbito 'global' ya fue creado en el constructor de FuncDirectory.
    pass

# --- Opcionales (Sin cambios) ---
def p_vars_opcional(p):
    '''vars_opcional : VARS lista_decl_var
                     | empty'''
    pass

def p_funcs_opcional(p):
    '''funcs_opcional : lista_funcs
                      | empty'''
    pass

# --- <VARS> y <TIPO> (Lógica de declaración - Sin cambios) ---
def p_lista_decl_var(p):
    '''lista_decl_var : decl_var
                      | decl_var lista_decl_var'''
    pass

def p_decl_var(p):
    'decl_var : ids DOSPTOS tipo PTOCOMA'
    # PN: Al final de la regla, registramos las variables
    lista_ids = p[1]
    tipo_var = p[3]
    try:
        for id_var in lista_ids:
            dir_general.add_var_to_func(ambito_actual, id_var, tipo_var)
    except Exception as e:
        print(f"Error en línea {p.lineno(1)}: {e}")
        sys.exit()

def p_ids(p):
    '''ids : ID
           | ids COMA ID'''
    if len(p) == 2:
        p[0] = [p[1]] 
    else:
        p[1].append(p[3]) 
        p[0] = p[1]

def p_tipo(p):
    '''tipo : ENTERO
            | FLOTANTE'''
    p[0] = p[1] # Devuelve 'entero' o 'flotante'

# --- <FUNCS> (Lógica de declaración - Sin cambios) ---
def p_lista_funcs(p):
    '''lista_funcs : func_def
                   | func_def lista_funcs'''
    pass

def p_func_def(p):
    'func_def : tipo_retorno pn_func_inicio ID LPAREN params RPAREN LBRACE vars_opcional cuerpo RBRACE pn_func_fin PTOCOMA'
    pass

def p_pn_func_inicio(p):
    'pn_func_inicio :'
    global ambito_actual
    tipo_retorno = p[-1]
    nombre_func = p.slice[1].value 
    
    try:
        dir_general.add_func(nombre_func, tipo_retorno)
        ambito_actual = nombre_func
    except Exception as e:
        print(f"Error en línea {p.lineno(1)}: {e}")
        sys.exit()

def p_pn_func_fin(p):
    'pn_func_fin :'
    global ambito_actual
    ambito_actual = 'global'

def p_tipo_retorno(p):
    '''tipo_retorno : tipo
                    | NULA'''
    p[0] = p[1]

def p_params(p):
    '''params : lista_params
              | empty'''
    pass

def p_lista_params(p):
    '''lista_params : ID DOSPTOS tipo pn_param
                    | lista_params COMA ID DOSPTOS tipo pn_param'''
    pass

def p_pn_param(p):
    'pn_param :'
    tipo_param = p[-1]
    nombre_param = p[-3]
    
    try:
        dir_general.add_var_to_func(ambito_actual, nombre_param, tipo_param)
        dir_general.add_param_to_func(ambito_actual, tipo_param)
    except Exception as e:
        print(f"Error en línea {p.lineno(1)}: {e}")
        sys.exit()

# --- <CUERPO> y <ESTATUTO> ---
def p_cuerpo(p):
    'cuerpo : LBRACE lista_estatuto RBRACE'
    pass

def p_lista_estatuto(p):
    '''lista_estatuto : estatuto lista_estatuto
                      | empty'''
    pass

def p_estatuto(p):
    '''estatuto : asigna
                | condicion
                | ciclo
                | imprime
                | llamada PTOCOMA
                | cuerpo'''
    pass

# --- Tipos de <ESTATUTO> (MODIFICADOS para Etapa 3) ---

def p_asigna(p):
    'asigna : ID ASIG pn_push_operador expresion PTOCOMA pn_gen_quad_asig'
    # p[1] = ID
    # p[2] = ASIG
    # p[3] = PN
    # p[4] = expresion (se resuelve y deja resultado en pilas)
    # p[5] = PTOCOMA
    # p[6] = PN de asignación
    pass

def p_pn_gen_quad_asig(p):
    'pn_gen_quad_asig :'
    # PN: Generar cuádruplo de asignación
    try:
        # 1. Pop el resultado de la expresión
        resultado_expr = quad_manager.pila_operandos.pop()
        tipo_expr = quad_manager.pila_tipos.pop()
        
        # 2. Pop el operador de asignación '='
        operador = quad_manager.pila_operadores.pop() # Debería ser '='
        
        # 3. Get el operando de la variable (el ID)
        # Lo tomamos del parser, p[-5] es el ID
        id_var = p[-5]
        tipo_var = dir_general.lookup_var_in_func(ambito_actual, id_var)
        
        # 4. Validar asignación con Cubo Semántico
        cubo_semantico.lookup(tipo_var, tipo_expr, operador)
        
        # 5. Generar cuádruplo
        quad_manager.agregar_cuadruplo(operador, resultado_expr, None, id_var)
        
    except Exception as e:
        print(f"Error en línea {p.lineno(1)}: {e}")
        sys.exit()

def p_imprime(p):
    'imprime : ESCRIBE pn_push_operador LPAREN lista_imprime RPAREN PTOCOMA'
    # p[2] es el PN que mete 'ESCRIBE' a POper
    pass

def p_lista_imprime(p):
    '''lista_imprime : item_imprime pn_gen_quad_imprime
                     | lista_imprime COMA item_imprime pn_gen_quad_imprime'''
    pass

def p_item_imprime(p):
    '''item_imprime : expresion
                    | LETRERO       
                    | LETRERO_KW'''
    # Si es 'expresion', se resuelve y deja el resultado en PilaO/PilaT
    # Si es LETRERO/LETRERO_KW, lo metemos a las pilas manualmente
    if p.slice[1].type != 'expresion':
        # p[1] es el string "hola" o la palabra "letrero"
        quad_manager.push_operando_tipo(p[1], 'letrero') # Usamos 'letrero' como tipo
        
def p_pn_gen_quad_imprime(p):
    'pn_gen_quad_imprime :'
    try:
        # 1. Pop el resultado
        resultado = quad_manager.pila_operandos.pop()
        quad_manager.pila_tipos.pop() # Pop el tipo, no lo usamos
        
        # 2. Generar cuádruplo
        # El operador 'ESCRIBE' debe estar en el fondo de la pila
        quad_manager.agregar_cuadruplo('ESCRIBE', None, None, resultado)
    except Exception as e:
        print(f"Error en línea {p.lineno(1)}: {e}")
        sys.exit()

def p_condicion(p):
    '''condicion : SI LPAREN expresion RPAREN cuerpo PTOCOMA
                 | SI LPAREN expresion RPAREN cuerpo SINO cuerpo PTOCOMA'''
    # Se elimina la lógica de Etapa 2.
    # Esta lógica (saltos) se implementará en la Etapa 4.
    pass

def p_ciclo(p):
    'ciclo : MIENTRAS LPAREN expresion RPAREN HAZ cuerpo PTOCOMA'
    # Se elimina la lógica de Etapa 2.
    # Esta lógica (saltos) se implementará en la Etapa 4.
    pass

def p_llamada(p):
    '''llamada : ID LPAREN RPAREN
               | ID LPAREN lista_args RPAREN'''
    # Se elimina la lógica de Etapa 2.
    # (PENDIENTE: Generar cuádruplos de llamada (ERA, PARAM, GO_SUB))
    pass

def p_lista_args(p):
    '''lista_args : expresion
                  | lista_args COMA expresion'''
    # (PENDIENTE: Generar cuádruplos PARAM)
    pass

# --- <EXPRESIÓN> (Nivel 4: Relacional) - MODIFICADO para Etapa 3 ---

def p_expresion(p):
    '''expresion : exp pn_expresion_relacional
                 | exp'''
    pass # Ya no devolvemos nada

def p_pn_expresion_relacional(p):
    'pn_expresion_relacional : OPREL pn_push_operador exp'
    # Este PN se ejecuta *después* de que 'exp' (p[3]) ha sido procesada
    # y ha dejado su resultado en las pilas.
    try:
        # Verificamos si el operador en el tope es relacional
        if quad_manager.pila_operadores:
            if quad_manager.pila_operadores[-1] in ('>', '<', '==', '!=', '>=', '<='):
                quad_manager.generar_cuadruplo_expresion()
    except Exception as e:
        print(f"Error en línea {p.lineno(1)}: {e}")
        sys.exit()

def p_oprel(p):
    '''OPREL : MAYOR
             | MENOR
             | DIF
             | IGUALDAD
             | MAYORIG
             | MENORIG'''
    # Esta regla es usada por 'pn_expresion_relacional'
    # NO es un PN, es solo un "atajo" para los tokens relacionales
    # El operador se mete a la pila en 'pn_push_operador'
    p[0] = p[1] # Devolvemos el string del operador

# --- <EXP> (Nivel 3: Aditivo) - MODIFICADO para Etapa 3 ---

def p_exp(p):
    '''exp : termino pn_check_op_aditivo
           | exp pn_push_op_aditivo termino pn_check_op_aditivo'''
    pass

def p_pn_push_op_aditivo(p):
    '''pn_push_op_aditivo : MAS pn_push_operador
                          | MENOS pn_push_operador'''
    pass # El PN 'pn_push_operador' ya hizo el trabajo

def p_pn_check_op_aditivo(p):
    'pn_check_op_aditivo :'
    # PN para verificar si hay sumas o restas pendientes
    try:
        if quad_manager.pila_operadores:
            if quad_manager.pila_operadores[-1] in ('+', '-'):
                quad_manager.generar_cuadruplo_expresion()
    except Exception as e:
        print(f"Error en línea {p.lineno(1)}: {e}")
        sys.exit()

# --- <TÉRMINO> (Nivel 2: Multiplicativo) - MODIFICADO para Etapa 3 ---

def p_termino(p):
    '''termino : factor pn_check_op_mult
               | termino pn_push_op_mult factor pn_check_op_mult'''
    pass

def p_pn_push_op_mult(p):
    '''pn_push_op_mult : POR pn_push_operador
                       | DIV pn_push_operador'''
    pass # El PN 'pn_push_operador' ya hizo el trabajo

def p_pn_check_op_mult(p):
    'pn_check_op_mult :'
    # PN para verificar si hay mult/div pendientes
    try:
        if quad_manager.pila_operadores:
            if quad_manager.pila_operadores[-1] in ('*', '/'):
                quad_manager.generar_cuadruplo_expresion()
    except Exception as e:
        print(f"Error en línea {p.lineno(1)}: {e}")
        sys.exit()

# --- <FACTOR> (Nivel 1: Base) - MODIFICADO para Etapa 3 ---

def p_factor_agrupacion(p):
    'factor : LPAREN pn_push_paren expresion RPAREN pn_pop_paren'
    pass

def p_pn_push_paren(p):
    'pn_push_paren :'
    quad_manager.push_operador('(') # Mete el 'fondo falso'

def p_pn_pop_paren(p):
    'pn_pop_paren :'
    try:
        quad_manager.pila_operadores.pop() # Saca el 'fondo falso'
    except Exception as e:
        print(f"Error: Desbalance de paréntesis - {e}")
        sys.exit()

def p_factor_unario(p):
    '''factor : MAS factor %prec UMAS
              | MENOS factor %prec UMENOS'''
    # (PENDIENTE: Lógica de cuádruplos para unarios)
    pass

def p_factor_llamada(p):
    'factor : llamada'
    # (PENDIENTE: Lógica de cuádruplos para llamadas)
    pass

def p_factor_id(p):
    'factor : ID'
    # PN: Meter operando y tipo a las pilas
    try:
        tipo_var = dir_general.lookup_var_in_func(ambito_actual, p[1])
        quad_manager.push_operando_tipo(p[1], tipo_var)
    except Exception as e:
        print(f"Error en línea {p.lineno(1)}: {e}")
        sys.exit()

def p_factor_cte(p):
    'factor : cte'
    # p[1] es la tupla (valor, tipo) que devuelve p_cte
    valor, tipo = p[1]
    quad_manager.push_operando_tipo(valor, tipo)

# --- <CTE> (Constantes) - MODIFICADO para Etapa 3 ---
def p_cte(p):
    '''cte : CTE_ENT
           | CTE_FLOT'''
    # Devolvemos una tupla (valor, tipo)
    if p.slice[1].type == 'CTE_ENT':
        p[0] = (p[1], 'entero')
    else:
        p[0] = (p[1], 'flotante')

# --- PN General para PUSH de Operadores ---
def p_pn_push_operador(p):
    'pn_push_operador :'
    # p[-1] es el token del operador que llamó a esta regla
    quad_manager.push_operador(p[-1])

# --- Regla 'empty' (Sin cambios) ---
def p_empty(p):
    'empty :'
    pass

# -----------------------------------------------------------
# 4. MANEJO DE ERRORES DE SINTAXIS (Sin cambios)
# -----------------------------------------------------------
def p_error(p):
    if p:
        print(f"Error de Sintaxis: Token inesperado '{p.value}' (tipo: {p.type}) en línea {p.lineno(0)}")
        parser.errok()
    else:
        print("Error de Sintaxis: Fin de archivo inesperado (EOF)")

# -----------------------------------------------------------
# 5. CONSTRUIR EL PARSER
# -----------------------------------------------------------
parser = yacc.yacc()

# -----------------------------------------------------------
# 6. SECCIÓN DE PRUEBA (MODIFICADO para Etapa 3)
# -----------------------------------------------------------
if __name__ == '__main__':
    # Lee el archivo de prueba
    try:
        # ===== ¡ASEGÚRATE DE USAR UN ARCHIVO DE PRUEBA DE ETAPA 3! =====
        with open('prueba_etapa3.pat', 'r') as f:
            data = f.read()
    except EOFError:
        print("No se pudo abrir el archivo de prueba.")
        data = ""
    except FileNotFoundError:
        print("Archivo 'prueba_etapa3.pat' no encontrado. Asegúrate de que existe.")
        data = ""

    if not data:
        print("No hay datos para analizar.")
    else:
        print("--- INICIO DE ANÁLISIS SINTÁCTICO ---")
        parser.parse(data, lexer=lexer)
        print("--- FIN DE ANÁLISIS SINTÁCTICO ---")
        
        # ===== ¡NUEVO! MOSTRAR CUÁDRUPLOS Y DIRECTORIO =====
        print("\n--- Directorio General Final ---")
        print(dir_general)
        
        quad_manager.mostrar_cuadruplos()