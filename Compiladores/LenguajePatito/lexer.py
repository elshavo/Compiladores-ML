# lexer.py
import ply.lex as lex

# --- Lista de tokens base (sin keywords) ---
tokens = (
    'ID', 'CTE_ENT', 'CTE_FLOT', 'LETRERO',
    'MAS', 'MENOS', 'POR', 'DIV',
    'ASIG',
    'MAYORIG', 'MENORIG', 'IGUALDAD', 'DIF', 'MAYOR', 'MENOR',
    'LPAREN', 'RPAREN', 'LBRACE', 'RBRACE', 'COMA', 'PTOCOMA',
    'DOSPTOS',
)

# --- Palabras reservadas ---
reservadas = {
    'programa':'PROGRAMA',
    'inicio':'INICIO',
    'fin':'FIN',
    'vars':'VARS',
    'nula':'NULA',
    'entero':'ENTERO',
    'flotante':'FLOTANTE',
    'escribe':'ESCRIBE',
    'letrero':'LETRERO_KW',
    'si':'SI',
    'sino':'SINO',
    'mientras':'MIENTRAS',
    'haz':'HAZ',
}
tokens = tokens + tuple(reservadas.values())

# --- Literales y operadores ---
t_MAYORIG  = r'>='
t_MENORIG  = r'<='
t_IGUALDAD = r'=='
t_DIF      = r'!='
t_MAYOR    = r'>'
t_MENOR    = r'<'

t_MAS     = r'\+'
t_MENOS   = r'-'
t_POR     = r'\*'
t_DIV     = r'/'
t_ASIG    = r'='

t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_LBRACE  = r'\{'
t_RBRACE  = r'\}'
t_COMA    = r','
t_PTOCOMA = r';'
t_DOSPTOS = r':'

def t_LETRERO(t):
    r'"[^"\n]*"'
    t.value = t.value[1:-1]
    return t

def t_CTE_FLOT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_CTE_ENT(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_ID(t):
    r'[A-Za-z_][A-Za-z_0-9]*'
    t.type = reservadas.get(t.value, 'ID')
    return t

# Espacios y nuevas líneas
t_ignore = ' \t'
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Comentarios de línea (opcional)
def t_comment(t):
    r'//[^\n]*'
    pass

def t_error(t):
    print(f"Caracter ilegal: {t.value[0]!r} en línea {t.lexer.lineno}")
    t.lexer.skip(1)

lexer = lex.lex()
