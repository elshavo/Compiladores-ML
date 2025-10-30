import ply.yacc as yacc
import sys

# 1. IMPORTAR LOS TOKENS DEL LEXER
# -----------------------------------------------------------
# Importa TODO de lexer.py. Es crucial que la variable 'tokens'
# y el objeto 'lexer' estén definidos en lexer.py
from lexer import *

# -----------------------------------------------------------
# 2. PRECEDENCIA DE OPERADORES
# -----------------------------------------------------------
# Definimos la precedencia que establecimos en la Etapa 0
# De menor a mayor precedencia
precedence = (
    ('left', 'MAYOR', 'MENOR', 'DIF', 'IGUALDAD', 'MAYORIG', 'MENORIG'), # Nivel 4: Relacionales
    ('left', 'MAS', 'MENOS'),                                         # Nivel 3: Aditivos
    ('left', 'POR', 'DIV'),                                           # Nivel 2: Multiplicativos
    ('right', 'UMAS', 'UMENOS')                                       # Nivel 1: Unarios (ficticios)
)

# -----------------------------------------------------------
# 3. DEFINICIÓN DE LA GRAMÁTICA (REGLAS CFG)
# -----------------------------------------------------------

# --- <Programa> ---
# El 'start' le dice a ply.yacc cuál es la regla inicial
start = 'programa'

def p_programa(p):
    'programa : PROGRAMA ID PTOCOMA vars_opcional funcs_opcional INICIO cuerpo FIN'
    print("¡Sintaxis de 'programa' correcta!")
    pass # En futuras etapas, aquí se construye el nodo raíz del AST

# --- Opcionales ---
def p_vars_opcional(p):
    '''vars_opcional : VARS lista_decl_var
                     | empty'''
    pass

def p_funcs_opcional(p):
    '''funcs_opcional : lista_funcs
                      | empty'''
    pass

# --- <VARS> y <TIPO> ---
def p_lista_decl_var(p):
    '''lista_decl_var : decl_var
                      | decl_var lista_decl_var'''
    pass

def p_decl_var(p):
    'decl_var : ids DOSPTOS tipo PTOCOMA'
    pass

def p_ids(p):
    '''ids : ID
           | ids COMA ID'''
    pass

def p_tipo(p):
    '''tipo : ENTERO
            | FLOTANTE'''
    pass

# --- <FUNCS> ---
def p_lista_funcs(p):
    '''lista_funcs : func_def
                   | func_def lista_funcs'''
    pass

def p_func_def(p):
    'func_def : tipo_retorno ID LPAREN params RPAREN LBRACE vars_opcional cuerpo RBRACE PTOCOMA'
    pass

def p_tipo_retorno(p):
    '''tipo_retorno : tipo
                    | NULA'''
    pass

def p_params(p):
    '''params : lista_params
              | empty'''
    pass

def p_lista_params(p):
    '''lista_params : ID DOSPTOS tipo
                    | lista_params COMA ID DOSPTOS tipo'''
    pass

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
                | cuerpo''' # (Extensión: bloques anidados)
    pass

# --- Tipos de <ESTATUTO> ---
def p_asigna(p):
    'asigna : ID ASIG expresion PTOCOMA'
    pass

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
                    | LETRERO_KW''' # (LETRERO es tu extensión)
    pass

def p_condicion(p):
    '''condicion : SI LPAREN expresion RPAREN cuerpo PTOCOMA
                 | SI LPAREN expresion RPAREN cuerpo SINO cuerpo PTOCOMA'''
    pass

def p_ciclo(p):
    'ciclo : MIENTRAS LPAREN expresion RPAREN HAZ cuerpo PTOCOMA'
    pass

def p_llamada(p):
    '''llamada : ID LPAREN RPAREN
               | ID LPAREN lista_args RPAREN'''
    pass

def p_lista_args(p):
    '''lista_args : expresion
                  | lista_args COMA expresion'''
    pass

# --- <EXPRESIÓN> (Nivel 4: Relacional) ---
def p_expresion(p):
    '''expresion : exp
                 | exp OPREL exp'''
    pass

def p_oprel(p):
    '''OPREL : MAYOR
             | MENOR
             | DIF
             | IGUALDAD
             | MAYORIG
             | MENORIG'''
    pass

# --- <EXP> (Nivel 3: Aditivo) ---
def p_exp(p):
    '''exp : termino
           | exp MAS termino
           | exp MENOS termino'''
    pass

# --- <TÉRMINO> (Nivel 2: Multiplicativo) ---
def p_termino(p):
    '''termino : factor
               | termino POR factor
               | termino DIV factor'''
    pass

# --- <FACTOR> (Nivel 1: Base) ---
def p_factor_agrupacion(p):
    'factor : LPAREN expresion RPAREN'
    pass

def p_factor_unario(p):
    '''factor : MAS factor %prec UMAS
              | MENOS factor %prec UMENOS'''
    # El %prec UMAS/UMENOS le dice a Yacc que use la precedencia
    # de los tokens "ficticios" UMAS/UMENOS (Nivel 1)
    pass

def p_factor_base(p):
    '''factor : llamada
              | ID
              | cte'''
    pass

# --- <CTE> (Constantes) ---
def p_cte(p):
    '''cte : CTE_ENT
           | CTE_FLOT'''
    pass

# --- Regla 'empty' ---
# Regla vacía (epsilon) para producciones opcionales
def p_empty(p):
    'empty :'
    pass

# -----------------------------------------------------------
# 4. MANEJO DE ERRORES DE SINTAXIS
# -----------------------------------------------------------
def p_error(p):
    if p:
        print(f"Error de Sintaxis: Token inesperado '{p.value}' (tipo: {p.type}) en línea {p.lineno}")
        # Se intenta recuperar del error
        parser.errok()
    else:
        print("Error de Sintaxis: Fin de archivo inesperado (EOF)")

# -----------------------------------------------------------
# 5. CONSTRUIR EL PARSER
# -----------------------------------------------------------
parser = yacc.yacc()

# -----------------------------------------------------------
# 6. SECCIÓN DE PRUEBA
# -----------------------------------------------------------
if __name__ == '__main__':
    # Lee el archivo de prueba
    try:
        with open('prueba.pat', 'r') as f:
            data = f.read()
    except EOFError:
        print("No se pudo abrir el archivo de prueba.")
        data = ""
    except FileNotFoundError:
        print("Archivo 'prueba.pat' no encontrado. Asegúrate de que existe.")
        data = ""

    if not data:
        print("No hay datos para analizar.")
    else:
        print("--- INICIO DE ANÁLISIS SINTÁCTICO ---")
        # Llama al parser.
        # El lexer se pasa como argumento (viene de la importación)
        parser.parse(data, lexer=lexer)
        print("--- FIN DE ANÁLISIS SINTÁCTICO ---")