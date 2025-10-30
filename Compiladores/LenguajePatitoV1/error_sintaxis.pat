programa mi_programa;
vars
    entero x;  // <-- ERROR SINTÁCTICO (debe ser 'x : entero;')

inicio
{
    x = 10  // <-- ERROR SINTÁCTICO (falta ';')
}
fin
Test-Case: error_lexico.pat (Cubre T-LEX-03)

programa mi_programa;
vars
    x : entero;
inicio
{
    // Error, @ no es un token válido
    x = 10 @ 5; 
}
fin
