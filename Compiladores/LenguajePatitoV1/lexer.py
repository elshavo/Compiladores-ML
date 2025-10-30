import ply.lex as lex
import sys

# ------------------------------------------------------------
# 1. LISTA DE TOKENS
# ------------------------------------------------------------
# Lista de todas las palabras reservadas (keywords)
reserved = {
    'programa': 'PROGRAMA',
    'inicio': 'INICIO',
    'fin': 'FIN',
    'vars': 'VARS',
    'entero': 'ENTERO',
    'flotante': 'FLOTANTE',
    'escribe': 'ESCRIBE',
    'letrero': 'LETRERO_KW',  # El 'letrero' keyword
    'si': 'SI',
    'sino': 'SINO',
    'mientras': 'MIENTRAS',
    'haz': 'HAZ',
    'nula': 'NULA'
}

# Lista completa de tokens, incluyendo las reservadas
tokens = [
    'ID',
    'CTE_ENT',
    'CTE_FLOT',
    'LETRERO',  # El string literal "hola"
    'MAS',
    'MENOS',
    'POR',
    'DIV',
    'ASIG',
    'MAYORIG',  # >=
    'MENORIG',  # <=
    'IGUALDAD', # ==
    'DIF',      # !=
    'MAYOR',    # >
    'MENOR',    # <
    'LPAREN',
    'RPAREN',
    'LBRACE',
    'RBRACE',
    'COMA',
    'PTOCOMA',
    'DOSPTOS'
] + list(reserved.values())

# ------------------------------------------------------------
# 2. TOKENS SIMPLES (EXPRESIONES REGULARES)
# ------------------------------------------------------------
# 't_' es el prefijo que ply.lex usa para tokens.
# El orden importa para los operadores de 2 caracteres (>=, <=, ==, !=)
# Deben ir ANTES que los de 1 caracter (>, <, =)
t_MAS = r'\+'
t_MENOS = r'-'
t_POR = r'\*'
t_DIV = r'/'
t_ASIG = r'='
t_MAYORIG = r'>='
t_MENORIG = r'<='
t_IGUALDAD = r'=='
t_DIF = r'!='
t_MAYOR = r'>'
t_MENOR = r'<'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_COMA = r','
t_PTOCOMA = r';'
t_DOSPTOS = r':'

# ------------------------------------------------------------
# 3. TOKENS COMPLEJOS (CON ACCIONES EN CÓDIGO)
# ------------------------------------------------------------

# Token para CTE_FLOT (constante flotante)
def t_CTE_FLOT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

# Token para CTE_ENT (constante entera)
def t_CTE_ENT(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Token para ID (identificadores) y palabras reservadas
def t_ID(t):
    r'[A-Za-z_][A-Za-z_0-9]*'
    # Revisa si el ID es una palabra reservada
    # t.type = reserved.get(t.value, 'ID')
    # Si 't.value' está en el diccionario 'reserved', cambia el tipo.
    # Si no, el tipo se queda como 'ID'.
    if t.value in reserved:
        t.type = reserved[t.value]
    return t

# Token para LETRERO (string literal, tu extensión)
def t_LETRERO(t):
    r'\"[^"\n]*\"'
    # Quita las comillas dobles del inicio y el final
    t.value = t.value[1:-1]
    return t

# Token para contar números de línea
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# ------------------------------------------------------------
# 4. REGLAS DE IGNORAR Y MANEJO DE ERRORES
# ------------------------------------------------------------

# Ignorar espacios en blanco y tabuladores
t_ignore = ' \t'

# Ignorar comentarios de línea (tu extensión)
t_ignore_COMMENT = r'//.*'

# Manejo de errores léxicos
# Se llama cuando se encuentra un carácter ilegal
def t_error(t):
    print(f"Error Léxico: Carácter ilegal '{t.value[0]}' en línea {t.lexer.lineno}")
    t.lexer.skip(1)

# ------------------------------------------------------------
# 5. CONSTRUIR EL LEXER
# ------------------------------------------------------------
lexer = lex.lex()

# ------------------------------------------------------------
# 6. SECCIÓN DE PRUEBA
# ------------------------------------------------------------
if __name__ == '__main__':
    # Lee el archivo de prueba (cambia 'prueba.pat' por tu archivo)
    try:
        with open('prueba.pat', 'r') as f:
            data = f.read()
    except EOFError:
        print("No se pudo abrir el archivo de prueba.")
        data = ""
    except FileNotFoundError:
        print("Archivo 'prueba.pat' no encontrado. Usando texto de ejemplo.")
        # Texto de ejemplo si no se encuentra el archivo
        data = """
        programa mi_programa;
        vars
            entero x, y;
            flotante z;
        
        inicio
        {
            // Esto es un comentario
            x = 10;
            y = 20;
            z = x + (y * 3.14);
            
            escribe("El valor de z es: ", z, letrero);
            
            si (z > 10.0) {
                escribe("Es mayor");
            } sino {
                escribe("Es menor o igual");
            }
        }
        fin
        """

    # Pasa el texto de entrada al lexer
    lexer.input(data)

    # Itera sobre el lexer para obtener todos los tokens
    print("--- INICIO DE ANÁLISIS LÉXICO ---")
    while True:
        tok = lexer.token()
        if not tok:
            break  # No hay más tokens
        print(tok)
    print("--- FIN DE ANÁLISIS LÉXICO ---")