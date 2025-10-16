from parser import parser

codigo = '''
programa p;
vars
  a: entero;
  b: flotante;
inicio {
  a = 3 + 2 * 5;
  si (a >= 10) { b = a - 1; } ;
  escribe("hola", a <= 20, a == 12, a != 7);
} fin
'''

arbol = parser.parse(codigo)
print(arbol)
