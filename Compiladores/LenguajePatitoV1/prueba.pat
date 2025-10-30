programa mi_programa;
vars
    // CORREGIDO: Formato "Ids : Tipo;"
    x, y : entero;
    z : flotante;

inicio
{
    // Esto es un comentario
    x = 10;
    y = 20;
    z = x + (y * 3.14);
    
    // CORREGIDO: Añadida coma faltante entre 'z' y 'letrero'
    escribe("El valor de z es: ", z, letrero);
    
    si (z > 10.0) {
        escribe("Es mayor");
    } sino {
        escribe("Es menor o igual");
    }
    // CORREGIDO: Añadido PTOCOMA al final del 'si/sino'
    ;
}
fin