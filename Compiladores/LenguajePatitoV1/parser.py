# -----------------------------------------------------------
# parser.py
#
# ETAPA 2 (Corregido)
# - Corregido el orden de argumentos en 'cubo_semantico.lookup()'
# - Eliminadas todas las etiquetas [cite]
# -----------------------------------------------------------

import ply.yacc as yacc
import sys

# --- 1. NUEVOS IMPORTS Y GLOBALES DE SEMÁNTICA ---

# Importa TODO de lexer.py (tokens)
from lexer import *
# Importamos nuestras clases de semántica
from directory import FuncDirectory
from semantic_cube import cubo_semantico

# --- Instancias Globales para Semántica ---
dir_general = FuncDirectory() # Nuestra instancia principal del Directorio
ambito_actual = 'global'      # Para saber en qué función estamos
tipo_actual = ''              # Variable temporal para guardar tipos

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

# --- <Programa> ---
start = 'programa'

def p_programa(p):
    'programa : PROGRAMA ID pn_programa_inicio PTOCOMA vars_opcional funcs_opcional INICIO cuerpo FIN'
    print("¡Sintaxis de 'programa' correcta!")
    
    # Para depuración: Imprime el directorio al final
    print("\n--- Directorio General Final ---")
    print(dir_general)
    print("--------------------------------")
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

# --- <VARS> y <TIPO> (Lógica de declaración) ---
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

# --- <FUNCS> (Lógica de declaración) ---
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

# --- Tipos de <ESTATUTO> (Validación Semántica) ---
def p_asigna(p):
    'asigna : ID ASIG expresion PTOCOMA'
    # PN: Validar asignación
    try:
        tipo_var = dir_general.lookup_var_in_func(ambito_actual, p[1])
        tipo_expr = p[3]
        
        # Consultar el cubo semántico para la asignación
        # ===== ¡CORREGIDO! =====
        cubo_semantico.lookup(tipo_var, tipo_expr, '=') 
        
    except Exception as e:
        print(f"Error en línea {p.lineno(1)}: {e}")
        sys.exit()

def p_imprime(p):
    'imprime : ESCRIBE LPAREN lista_imprime RPAREN PTOCOMA'
    pass

def p_lista_imprime(p):
    '''lista_imprime : item_imprime
                     | lista_imprime COMA item_imprime'''
    pass

def p_item_imprime(p):
    '''item_imprime : expresion
                    | LETRERO       
                    | LETRERO_KW'''
    pass

def p_condicion(p):
    '''condicion : SI LPAREN expresion RPAREN cuerpo PTOCOMA
                 | SI LPAREN expresion RPAREN cuerpo SINO cuerpo PTOCOMA'''
    # PN: Validar que la expresión sea booleana
    tipo_expr = p[3]
    if tipo_expr != 'booleano':
        print(f"Error en línea {p.lineno(1)}: Error Semántico. La expresión en un 'si' debe ser booleana, no '{tipo_expr}'.")
        sys.exit()

def p_ciclo(p):
    'ciclo : MIENTRAS LPAREN expresion RPAREN HAZ cuerpo PTOCOMA'
    # PN: Validar que la expresión sea booleana
    tipo_expr = p[3]
    if tipo_expr != 'booleano':
        print(f"Error en línea {p.lineno(1)}: Error Semántico. La expresión en un 'mientras' debe ser booleana, no '{tipo_expr}'.")
        sys.exit()

def p_llamada(p):
    '''llamada : ID LPAREN RPAREN
               | ID LPAREN lista_args RPAREN'''
    # PN: Validar llamada a función
    try:
        # 1. Validar que la función existe
        dir_general.lookup_func(p[1])
        
        # (PENDIENTE: Validar número y tipo de argumentos en p[3])
        
        # 3. Devolver el tipo de retorno de la función
        tipo_retorno = dir_general.functions[p[1]]['tipo_retorno']
        
        # 4. Validar que no se use una función 'nula' en una expresión
        if tipo_retorno == 'nula':
             print(f"Error en línea {p.lineno(1)}: Error Semántico. La función '{p[1]}' (tipo 'nula') no puede ser usada en una expresión.")
             sys.exit()
             
        p[0] = tipo_retorno # Devolvemos el tipo de retorno
        
    except Exception as e:
        print(f"Error en línea {p.lineno(1)}: {e}")
        sys.exit()

def p_lista_args(p):
    '''lista_args : expresion
                  | lista_args COMA expresion'''
    # (PENDIENTE: Devolver una lista de tipos de argumentos)
    pass

# --- <EXPRESIÓN> (Nivel 4: Relacional) - VALIDACIÓN ---
def p_expresion(p):
    '''expresion : exp
                 | exp OPREL exp'''
    if len(p) == 2:
        p[0] = p[1] # Pasa el tipo de 'exp' hacia arriba
    else:
        # PN: Validar expresión relacional
        try:
            tipo_izq = p[1]
            tipo_der = p[3]
            operador = p[2] 
            
            # ===== ¡CORREGIDO! =====
            tipo_res = cubo_semantico.lookup(tipo_izq, tipo_der, operador)
            p[0] = tipo_res # Debería ser 'booleano'
            
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
    p[0] = p[1] # Devuelve '>', '<', '==', etc.

# --- <EXP> (Nivel 3: Aditivo) - VALIDACIÓN ---
def p_exp(p):
    '''exp : termino
           | exp MAS termino
           | exp MENOS termino'''
    if len(p) == 2:
        p[0] = p[1] # Pasa el tipo de 'termino'
    else:
        # PN: Validar expresión aditiva
        try:
            tipo_izq = p[1]
            tipo_der = p[3]
            operador = p[2] # '+' o '-'
            
            # ===== ¡CORREGIDO! =====
            tipo_res = cubo_semantico.lookup(tipo_izq, tipo_der, operador)
            p[0] = tipo_res # Debería ser 'entero' o 'flotante'
            
        except Exception as e:
            print(f"Error en línea {p.lineno(1)}: {e}")
            sys.exit()

# --- <TÉRMINO> (Nivel 2: Multiplicativo) - VALIDACIÓN ---
def p_termino(p):
    '''termino : factor
               | termino POR factor
               | termino DIV factor'''
    if len(p) == 2:
        p[0] = p[1] # Pasa el tipo de 'factor'
    else:
        # PN: Validar expresión multiplicativa
        try:
            tipo_izq = p[1]
            tipo_der = p[3]
            operador = p[2] # '*' o '/'
            
            # ===== ¡CORREGIDO! =====
            tipo_res = cubo_semantico.lookup(tipo_izq, tipo_der, operador)
            p[0] = tipo_res # Debería ser 'entero' o 'flotante'
            
        except Exception as e:
            print(f"Error en línea {p.lineno(1)}: {e}")
            sys.exit()

# --- <FACTOR> (Nivel 1: Base) - VALIDACIÓN ---
def p_factor_agrupacion(p):
    'factor : LPAREN expresion RPAREN'
    p[0] = p[2] # Pasa el tipo de la 'expresion' interna

def p_factor_unario(p):
    '''factor : MAS factor %prec UMAS
              | MENOS factor %prec UMENOS'''
    # PN: Validar que el unario se aplique a un número
    tipo_factor = p[2]
    if tipo_factor not in ('entero', 'flotante'):
        print(f"Error en línea {p.lineno(1)}: Error Semántico. El operador unario '{p[1]}' solo se puede aplicar a 'entero' o 'flotante', no a '{tipo_factor}'.")
        sys.exit()
    p[0] = tipo_factor

def p_factor_llamada(p):
    'factor : llamada'
    p[0] = p[1] # 'llamada' ya devuelve su tipo de retorno

def p_factor_id(p):
    'factor : ID'
    # PN: Es un ID, buscar su tipo
    try:
        tipo_var = dir_general.lookup_var_in_func(ambito_actual, p[1])
        p[0] = tipo_var # Devolver el tipo de la variable
    except Exception as e:
        print(f"Error en línea {p.lineno(1)}: {e}")
        sys.exit()

def p_factor_cte(p):
    'factor : cte'
    p[0] = p[1] # 'cte' ya devuelve su tipo ('entero' o 'flotante')

# --- <CTE> (Constantes) - VALIDACIÓN ---
def p_cte(p):
    '''cte : CTE_ENT
           | CTE_FLOT'''
    # PN: Devolver el TIPO de la constante
    if p.slice[1].type == 'CTE_ENT':
        p[0] = 'entero'
    else:
        p[0] = 'flotante'

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
# 6. SECCIÓN DE PRUEBA (Sin cambios)
# -----------------------------------------------------------
if __name__ == '__main__':
    # Lee el archivo de prueba
    try:
        # Asegúrate de que este nombre de archivo sea el correcto para tus pruebas
        with open('prueba_semantica.pat', 'r') as f:
            data = f.read()
    except EOFError:
        print("No se pudo abrir el archivo de prueba.")
        data = ""
    except FileNotFoundError:
        print("Archivo 'prueba_semantica.pat' no encontrado. Asegúrate de que existe.")
        data = ""

    if not data:
        print("No hay datos para analizar.")
    else:
        print("--- INICIO DE ANÁLISIS SINTÁTICO ---")
        parser.parse(data, lexer=lexer)
        print("--- FIN DE ANÁLISIS SINTÁTICO ---")