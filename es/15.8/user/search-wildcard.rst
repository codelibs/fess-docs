===========================
Búsqueda con comodines
===========================

Puede utilizar comodines de un carácter o múltiples caracteres dentro de los términos de búsqueda. ? se puede especificar como comodín de un carácter, y \* se puede especificar como comodín de múltiples caracteres. Los comodines se pueden utilizar en palabras. No es posible realizar búsquedas con comodines en oraciones.

Cómo utilizar
-------------

Para utilizar un comodín de un carácter, use ? de la siguiente manera:

::

    te?t

En el caso anterior, se tratará como un comodín de un carácter, como text o test.

Para utilizar un comodín de múltiples caracteres, use \* de la siguiente manera:

::

    test*

En el caso anterior, se tratará como un comodín de múltiples caracteres, como test, tests o tester. Además,

::

    te*t

también se puede utilizar dentro del término de búsqueda.

Condiciones de uso
------------------

Los comodines se utilizan para cadenas de texto registradas en el índice.
Por lo tanto, si el índice se crea con bi-gram u otros métodos, el japonés se tratará como cadenas de longitud fija sin significado, por lo que los comodines en japonés no funcionarán como se espera.
Si desea utilizar comodines en japonés, utilícelos en campos que usen análisis morfológico.
