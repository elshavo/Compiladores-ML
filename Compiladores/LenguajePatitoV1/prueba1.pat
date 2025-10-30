programa mi_programa;
vars
    x, y : entero;
    z : flotante;
inicio
{
    // Prueba de asignación y precedencia
    x = 10;
    z = x + (y * 3.14);

    // Prueba de E/S con extensión de string
    escribe("El valor de z es: ", z, letrero);

    // Prueba de condición
    si (z > 10.0) {
        escribe("Es mayor");
    } sino {
        escribe("Es menor o igual");
    }
    ; // Punto y coma de la condición
}
Fin
