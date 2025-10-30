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