programa test8;
vars
    x, y : entero;
    z : flotante;
inicio
{
    x = 10;
    y = 20;
    
    // (10 > (20 + 1)) -> (10 > 21) -> t1 = false
    escribe(x > (y + 1)); 
    
    // z = 10.5 + 10
    z = 10.5 + x;
    escribe(z);
}
fin