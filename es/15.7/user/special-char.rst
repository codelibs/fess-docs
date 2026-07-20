=====================
Caracteres especiales
=====================

En las búsquedas de |Fess|, los siguientes símbolos se tratan como caracteres especiales (palabras reservadas) de la sintaxis de búsqueda. Si desea buscar estos símbolos como caracteres de búsqueda normales, es necesario escaparlos. Por ejemplo, si busca directamente símbolos como "/" o ":" incluidos en una URL o ruta de archivo, o "+" o "-" que aparecen en código de programación, puede obtener resultados de búsqueda no deseados. Consulte a continuación el método de escape.

::

    + - && || ! ( ) { } [ ] ^ " ~ * ? : \ /


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
     - Búsqueda con boost (ponderación)
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

Escape con \ o encierre el término de búsqueda entre comillas ".

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

