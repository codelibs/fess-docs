=====================
Caracteres especiales
=====================

Los siguientes caracteres tienen un significado especial en la sintaxis de las consultas de búsqueda, por lo que se tratan como caracteres especiales en los términos de búsqueda. Para utilizar estos caracteres como caracteres de búsqueda literales, es necesario escaparlos.

::

    + - && || ! ( ) { } [ ] ^ " ~ * ? : \ /

Estos caracteres se utilizan para invocar funciones de búsqueda como términos obligatorios/prohibidos (``+`` ``-``), operadores booleanos (``&&`` ``||`` ``!``), agrupación (``( )``), búsqueda por rango (``[ ]`` ``{ }``), búsqueda con impulso (boost) (``^``), búsqueda de frases (``"``), búsqueda difusa (fuzzy) (``~``), búsqueda con comodines (``*`` ``?``) y búsqueda por campo (``:``).


Cómo utilizar
-------------

Para tratar un carácter especial como un carácter de búsqueda literal, utilice uno de los siguientes métodos.

* Coloque ``\`` inmediatamente antes del carácter para escaparlo. El único carácter que sigue se trata como un carácter normal en lugar de sintaxis de consulta.
* Encierre el término de búsqueda entre ``"``. La cadena encerrada se trata como una búsqueda de frase, y los caracteres especiales que contiene no se interpretan como sintaxis de consulta. Tenga en cuenta, sin embargo, que al convertirse en una búsqueda de frase, funciones como la búsqueda con comodines (``*`` ``?``) no están disponibles.

::

    aaa\/bbb
    "aaa/bbb"
