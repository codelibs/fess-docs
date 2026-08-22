=====================
Caracteres especiales
=====================

Los siguientes caracteres tienen un significado especial en la sintaxis de las consultas de búsqueda, por lo que se tratan como caracteres especiales en los términos de búsqueda. Para utilizar estos caracteres como caracteres de búsqueda literales, es necesario escaparlos.

::

    + - && || ! ( ) { } [ ] ^ " ~ * ? : \ /

Estos caracteres se utilizan para invocar funciones de búsqueda como términos obligatorios/prohibidos (``+`` ``-``), operadores booleanos (``&&`` ``||`` ``!``), agrupación (``( )``), búsqueda por rango (``[ ]`` ``{ }``), búsqueda con impulso (boost) (``^``), búsqueda de frases (``"``), búsqueda difusa (fuzzy) (``~``), búsqueda con comodines (``*`` ``?``) y búsqueda por campo (``:``).

Por ejemplo, si busca directamente símbolos como "/" o ":" incluidos en una URL o ruta de archivo, o "+" o "-" que aparecen en código de programación, puede obtener resultados de búsqueda no deseados. Consulte a continuación el método de escape.


Lista de caracteres especiales y su significado
-------------------------------------------------

.. list-table::
   :header-rows: 1

   * - Carácter especial
     - Significado
     - Página relacionada
   * - ``+`` ``-``
     - Indica un término obligatorio o excluido (búsqueda AND / búsqueda NOT)
     - :doc:`search-and` / :doc:`search-not`
   * - ``&&`` ``||``
     - Búsqueda AND / búsqueda OR
     - :doc:`search-and` / :doc:`search-or`
   * - ``!``
     - Búsqueda NOT (búsqueda de exclusión)
     - :doc:`search-not`
   * - ``( )``
     - Agrupación de condiciones de búsqueda
     - :doc:`advanced-search`
   * - ``[ ]`` ``{ }``
     - Búsqueda por rango (``[ ]`` incluye los límites, ``{ }`` los excluye)
     - :doc:`search-range`
   * - ``^``
     - Búsqueda con impulso (boost)
     - :doc:`search-boost`
   * - ``"``
     - Búsqueda de frases (trata el texto entre comillas como una sola unidad; también puede usarse en lugar del escape)
     - :doc:`advanced-search`
   * - ``~``
     - Búsqueda difusa (búsqueda aproximada)
     - :doc:`search-fuzzy`
   * - ``*`` ``?``
     - Búsqueda con comodines
     - :doc:`search-wildcard`
   * - ``:``
     - Especificación del campo de búsqueda
     - :doc:`search-field`
   * - ``\``
     - Carácter de escape
     - (esta página)
   * - ``/``
     - Barra (debe escaparse si aparece, por ejemplo, en una URL)
     - :doc:`search-field`


Cómo utilizar
-------------

Para tratar un carácter especial como un carácter de búsqueda literal, utilice uno de los siguientes métodos.

* Coloque ``\`` inmediatamente antes del carácter para escaparlo. El único carácter que sigue se trata como un carácter normal en lugar de sintaxis de consulta.
* Encierre el término de búsqueda entre ``"``. La cadena encerrada se trata como una búsqueda de frase, y los caracteres especiales que contiene no se interpretan como sintaxis de consulta. Tenga en cuenta, sin embargo, que al convertirse en una búsqueda de frase, funciones como la búsqueda con comodines (``*`` ``?``) no están disponibles.

::

    aaa\/bbb
    "aaa/bbb"

Por ejemplo, si desea buscar el término "C++" tal como es, puede escaparlo de la siguiente manera:

::

    C\+\+
    "C++"


Véase también
-------------

- :doc:`search-field` - Búsqueda con especificación de campos
- :doc:`search-wildcard` - Búsqueda con comodines
- :doc:`search-fuzzy` - Búsqueda difusa
- :doc:`advanced-search` - Búsqueda avanzada
