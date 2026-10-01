========================
Búsqueda de proximidad
========================
Búsqueda de proximidad (distancia entre palabras)
===================================================

La búsqueda de proximidad permite encontrar documentos en los que las palabras de una frase aparecen cerca unas de otras, aunque no estén juntas. Es útil cuando pueden aparecer otras palabras entre las que se están buscando.

Cómo utilizar
---------------

Encierre las palabras entre comillas dobles y agregue "~" y un número después de la comilla de cierre.

Por ejemplo, la siguiente búsqueda encuentra documentos en los que "Fess" y "búsqueda" aparecen a una distancia de 3 o menos:

::

    "Fess búsqueda"~3

El número es la cantidad máxima de desplazamientos de posición permitidos entre las palabras (consulte "Cómo se cuenta la distancia" más adelante). Cuanto mayor sea el número, más separadas pueden estar las palabras.

También puede realizar una búsqueda de proximidad en un campo específico. En el siguiente ejemplo, se busca en el campo title.

::

    title:"Fess búsqueda"~3

Si omite el número y especifica únicamente "~" (por ejemplo, ``"Fess búsqueda"~``), la frase se busca como una frase normal en la que las palabras deben ser contiguas. Un número decimal se trunca a un entero (``~2.5`` se trata como ``~2``).

La búsqueda de proximidad se puede combinar con un impulso (boost). En el siguiente ejemplo, la búsqueda de proximidad se multiplica por 2 (consulte :doc:`search-boost`).

::

    "Fess búsqueda"~5^2

Cómo se cuenta la distancia
-----------------------------

* El número es la cantidad máxima de desplazamientos de posición permitidos entre las palabras. Se cuenta en tokens generados por el analizador del campo de destino, no en caracteres ni en palabras separadas por espacios. En textos en inglés, equivale aproximadamente al número de palabras que hay entre los términos. Las palabras eliminadas como palabras vacías (stop words) durante el análisis también se cuentan.
* Las palabras pueden aparecer en otro orden, pero el orden inverso requiere un número mayor. Por ejemplo, un documento que contiene "quick brown fox" coincide con ``"quick fox"~1``, pero solo coincide con ``"fox quick"`` a partir de ``~3``.

::

    "quick fox"~1
    "fox quick"~3

Texto en japonés, chino y coreano (CJK)
-----------------------------------------

En textos en japonés y otros textos CJK, la unidad en que se cuenta la distancia depende del campo.

* En los campos generales title y content, la distancia es cercana al número de caracteres que hay entre las palabras.
* En los campos específicos de cada idioma, la distancia se cuenta en tokens morfológicos, y las partículas eliminadas también se cuentan.

Por ello, separe las palabras con espacios y especifique un número generoso.

::

    "全文 検索"~5
    "大阪 おいしい"~10

Es posible que una cadena sin espacios (por ejemplo, ``"大阪おいしい"~10``) no funcione como se espera como búsqueda de proximidad entre palabras, ya que en los campos generales se compara como una única cadena continua. Separe las palabras con espacios. La distancia no se puede convertir exactamente en un número de caracteres, por lo que conviene empezar con un número generoso y reducirlo a medida que comprueba los resultados.

Véase también
===============

- :doc:`search-fuzzy` - Búsqueda difusa
- :doc:`search-boost` - Búsqueda con boost
- :doc:`search-field` - Búsqueda con especificación de campos
- :doc:`special-char` - Caracteres especiales
