import ply.yacc as yacc
from lexer import tokens

# ---------------------------------------------------------
# Precedencias: relacionales más bajas que +-, y estos más bajos que */.
# ---------------------------------------------------------
precedence = (
    ('left', 'MAYOR', 'MENOR', 'DIF', 'IGUALDAD', 'MAYORIG', 'MENORIG'),
    ('left', 'MAS', 'MENOS'),
    ('left', 'POR', 'DIV'),
)

# ---------------------------------------------------------
# PROGRAMA
# Programa → 'programa' id ';' Vars Funcs? 'inicio' Cuerpo 'fin'
# (por ahora ignoramos Funcs; lo añadiremos después)
# ---------------------------------------------------------
def p_Programa(p):
    'Programa : PROGRAMA ID PTOCOMA Vars INICIO Cuerpo FIN'
    p[0] = ('programa', p[2], p[4], p[6])

# ---------------------------------------------------------
# VARS
# Vars → 'vars' ListaDeclVar | ε
# ListaDeclVar → id ':' Tipo ';' ListaDeclVar | id ':' Tipo ';'
# Tipo → 'entero' | 'flotante'
# ---------------------------------------------------------
def p_Vars(p):
    '''Vars : VARS ListaDeclVar
            | empty'''
    p[0] = ('vars', p[2]) if len(p) == 3 else ('vars', [])

def p_ListaDeclVar_rec(p):
    'ListaDeclVar : ID DOSPTOS Tipo PTOCOMA ListaDeclVar'
    p[0] = [(p[1], p[3])] + p[5]

def p_ListaDeclVar_base(p):
    'ListaDeclVar : ID DOSPTOS Tipo PTOCOMA'
    p[0] = [(p[1], p[3])]

def p_Tipo(p):
    '''Tipo : ENTERO
            | FLOTANTE'''
    # p[1] es el lexema 'entero'/'flotante'
    p[0] = p[1].lower()

# ---------------------------------------------------------
# CUERPO y ESTATUTOS
# Cuerpo → '{' ListaEstatuto '}'
# ListaEstatuto → Estatuto ListaEstatuto | ε
# Estatuto → Asigna | Condicion | Ciclo | Imprime ';' | Llamada ';' | Cuerpo
# ---------------------------------------------------------
def p_Cuerpo(p):
    'Cuerpo : LBRACE ListaEstatuto RBRACE'
    p[0] = ('cuerpo', p[2])

def p_ListaEstatuto_rec(p):
    'ListaEstatuto : Estatuto ListaEstatuto'
    p[0] = [p[1]] + p[2]

def p_ListaEstatuto_empty(p):
    'ListaEstatuto : empty'
    p[0] = []

def p_Estatuto(p):
    '''Estatuto : Asigna
                | Condicion
                | Ciclo
                | Imprime PTOCOMA
                | Llamada PTOCOMA
                | Cuerpo'''
    p[0] = p[1] if len(p) == 2 else ('stmt', p[1])

# ---------------------------------------------------------
# ASIGNACION
# Asigna → id '=' Expresion ';'
# ---------------------------------------------------------
def p_Asigna(p):
    'Asigna : ID ASIG Expresion PTOCOMA'
    p[0] = ('asigna', p[1], p[3])

# ---------------------------------------------------------
# IMPRIME
# Imprime → 'escribe' '(' ListaImprime ')'
# ListaImprime → ItemImprime (',' ItemImprime)*
# ItemImprime → Expresion | LETRERO   | (opcional) LETRERO_KW
# ---------------------------------------------------------
def p_Imprime(p):
    'Imprime : ESCRIBE LPAREN ListaImprime RPAREN'
    p[0] = ('imprime', p[3])

def p_ListaImprime_uno(p):
    'ListaImprime : ItemImprime'
    p[0] = [p[1]]

def p_ListaImprime_mas(p):
    'ListaImprime : ListaImprime COMA ItemImprime'
    p[0] = p[1] + [p[3]]

def p_ItemImprime(p):
    '''ItemImprime : Expresion
                   | LETRERO
                   | LETRERO_KW'''
    # Si viene LETRERO (string literal) lo marcamos distinto
    if isinstance(p[1], tuple):
        p[0] = p[1]
    else:
        p[0] = ('str', p[1])

# ---------------------------------------------------------
# CONDICION (IF)
# Condicion → 'si' '(' Expresion ')' Cuerpo ';'
#           | 'si' '(' Expresion ')' Cuerpo 'sino' Cuerpo ';'
# ---------------------------------------------------------
def p_Condicion_sin_sino(p):
    'Condicion : SI LPAREN Expresion RPAREN Cuerpo PTOCOMA'
    p[0] = ('if', p[3], p[5], None)

def p_Condicion_con_sino(p):
    'Condicion : SI LPAREN Expresion RPAREN Cuerpo SINO Cuerpo PTOCOMA'
    p[0] = ('if', p[3], p[5], p[7])

# ---------------------------------------------------------
# CICLO (WHILE)
# Ciclo → 'mientras' '(' Expresion ')' 'haz' Cuerpo ';'
# ---------------------------------------------------------
def p_Ciclo(p):
    'Ciclo : MIENTRAS LPAREN Expresion RPAREN HAZ Cuerpo PTOCOMA'
    p[0] = ('while', p[3], p[6])

# ---------------------------------------------------------
# LLAMADA
# Llamada → id '(' ListaArgs? ')'
# ListaArgs → Expresion (',' Expresion)*
# ---------------------------------------------------------
def p_Llamada_vacia(p):
    'Llamada : ID LPAREN RPAREN'
    p[0] = ('call', p[1], [])

def p_Llamada_args(p):
    'Llamada : ID LPAREN ListaArgs RPAREN'
    p[0] = ('call', p[1], p[3])

def p_ListaArgs_uno(p):
    'ListaArgs : Expresion'
    p[0] = [p[1]]

def p_ListaArgs_mas(p):
    'ListaArgs : ListaArgs COMA Expresion'
    p[0] = p[1] + [p[3]]

# ---------------------------------------------------------
# EXPRESION / EXP / TERMINO / FACTOR
# Expresion → Exp | Exp Oprel Exp
# ---------------------------------------------------------
def p_Expresion_rel(p):
    '''Expresion : Exp
                 | Exp Oprel Exp'''
    p[0] = p[1] if len(p) == 2 else ('rel', p[2], p[1], p[3])

def p_Oprel(p):
    '''Oprel : MAYOR
             | MENOR 
             | DIF 
             | IGUALDAD 
             | MAYORIG 
             | MENORIG'''
    p[0] = p[1]

def p_Exp(p):
    '''Exp : Exp MAS Termino
           | Exp MENOS Termino
           | Termino'''
    p[0] = ('bin', p[2], p[1], p[3]) if len(p) == 4 else p[1]

def p_Termino(p):
    '''Termino : Termino POR Factor
               | Termino DIV Factor
               | Factor'''
    p[0] = ('bin', p[2], p[1], p[3]) if len(p) == 4 else p[1]

def p_Factor_paren(p):
    'Factor : LPAREN Expresion RPAREN'
    p[0] = p[2]

def p_Factor_unario(p):
    '''Factor : MAS Factor
              | MENOS Factor'''
    p[0] = ('un', p[1], p[2])

def p_Factor_base(p):
    '''Factor : ID
              | CTE_ENT
              | CTE_FLOT'''
    if isinstance(p[1], str):
        p[0] = ('id', p[1])
    else:
        p[0] = ('cte', p[1])

# ---------------------------------------------------------
def p_empty(p):
    'empty :'
    p[0] = None

def p_error(p):
    if p:
        print(f"[SyntaxError] token={p.type} value={p.value!r}")
    else:
        print("[SyntaxError] Fin de entrada inesperado")

parser = yacc.yacc()
