================
Búsqueda difusa
================

Búsqueda difusa (búsqueda aproximada)
======================================

Cuando desee buscar también palabras que no coincidan exactamente con el término de búsqueda, puede utilizar la búsqueda difusa (búsqueda aproximada). La búsqueda difusa es un método de búsqueda que considera coincidente una palabra registrada en el índice si la diferencia (distancia de edición) con respecto al término de búsqueda se encuentra dentro de un rango determinado. La distancia de edición es el número mínimo de operaciones de inserción, eliminación o sustitución de caracteres necesarias para transformar una palabra en otra. De forma predeterminada, |Fess| utiliza la distancia de Damerau-Levenshtein (optimal string alignment), que, además de estas operaciones, cuenta también el intercambio de dos caracteres adyacentes como una única diferencia.

Cómo utilizar
--------------

Para aplicar la búsqueda difusa, agregue "~" después del término de búsqueda.

Por ejemplo, si desea realizar una búsqueda difusa de la palabra "fess", puede buscar documentos que contengan palabras similares a "fess" (como "fes") ingresando lo siguiente en el formulario de búsqueda:

::

    fess~

Si agrega un número después de "~", puede especificar la distancia de edición permitida (cuántos caracteres de diferencia se toleran). Los valores que se pueden especificar son los números enteros 0, 1 o 2.

::

    fess~1

En el ejemplo anterior, se buscan palabras cuya distancia de edición con respecto a "fess" sea de 1 o menos.

Si omite el número y especifica únicamente "~", se considera una distancia de edición de 2. El valor máximo de la distancia de edición es 2, por lo que, aunque especifique un valor de 3 o superior, también se tratará como 2.

También puede realizar una búsqueda difusa especificando un campo. En el siguiente ejemplo, se buscan documentos que contengan, en el campo title, palabras similares a "fess".

::

    title:fess~

Si no especifica ningún campo, la búsqueda difusa se realiza sobre los campos title y content.

Condiciones de uso
--------------------

Tenga en cuenta los siguientes puntos al utilizar la búsqueda difusa.

* La búsqueda difusa se aplica a nivel de palabra. No se puede aplicar a frases entre comillas. Además, un número agregado después de una frase (por ejemplo, ``"Fess Search"~2``) no corresponde a una búsqueda difusa, sino a una :doc:`búsqueda de proximidad <search-proximity>` que indica la distancia entre palabras.
* La búsqueda difusa se realiza sobre las palabras registradas en el índice y el término de búsqueda no se vuelve a analizar. Por ello, es posible que no funcione como se espera en textos como el japonés, que se tokeniza mediante bi-gramas o análisis morfológico. La búsqueda difusa es eficaz principalmente con palabras alfanuméricas.
* El término de una búsqueda difusa cuenta la distancia de edición tal cual, incluida la distinción entre mayúsculas y minúsculas. Como las palabras alfabéticas registradas en el índice normalmente se convierten a minúsculas, utilice minúsculas en el término de búsqueda. Por ejemplo, ``Fess~1`` agota la distancia de edición 1 solo con la ``F`` mayúscula inicial, por lo que no da el mismo resultado que ``fess~1``. Además, ``Fess~0`` no coincide con nada, porque no hay en el índice ninguna palabra que coincida con la palabra en mayúsculas ``Fess`` (``fess~0`` en minúsculas es una coincidencia exacta).
* Si agrega "~" (distancia de edición 2) a palabras muy cortas, de 1 o 2 caracteres, también coinciden palabras en las que solo se han sustituido tantos caracteres como casi la longitud de la palabra. Por ejemplo, ``ab~`` coincide con ``ab`` y ``ac`` y también con ``xy``, que difiere en los dos caracteres. Como esto aumenta los resultados no deseados, especifique una distancia de edición pequeña para las palabras cortas, como ``ab~1``.

.. note::

    El comportamiento de la búsqueda difusa se puede ajustar en ``fess_config.properties``.

    * ``query.fuzzy.prefix_length`` (valor predeterminado: ``0``): número de caracteres desde el principio que deben coincidir exactamente. Si aumenta este valor, se reduce el margen de tolerancia a errores.
    * ``query.fuzzy.expansions`` (valor predeterminado: ``50``): número máximo de palabras que se expanden como candidatas de coincidencia.
    * ``query.fuzzy.transpositions`` (valor predeterminado: ``true``): especifica si el intercambio de dos caracteres adyacentes se cuenta como una única edición. Si es ``true``, se utiliza la distancia de Damerau-Levenshtein (optimal string alignment); si es ``false``, se utiliza la distancia de Levenshtein clásica.

.. note::

    Incluso en una búsqueda normal sin "~", |Fess| agrega automáticamente, como ayuda adicional, una ligera coincidencia difusa ponderada (``query.boost.fuzzy.*``) para los términos de búsqueda que tengan una longitud igual o superior a un valor determinado (de forma predeterminada, 4 caracteres o más), con el fin de mejorar la relevancia. Esta es una función destinada principalmente a ajustar la clasificación de los resultados de búsqueda y es un mecanismo distinto de la búsqueda difusa mediante "~". Sin embargo, esta coincidencia auxiliar también se incluye en los resultados de búsqueda, por lo que pueden añadirse a los resultados documentos que solo contienen una palabra que difiere en un carácter y no contienen el propio término de búsqueda (los documentos que contienen el propio término de búsqueda aparecen en posiciones superiores). Si desea desactivar este comportamiento, especifique un valor negativo (por ejemplo, ``-1``) en ``query.boost.fuzzy.min.length``.


Véase también
=============

- :doc:`search-wildcard` - Búsqueda con comodines
- :doc:`search-proximity` - Búsqueda de proximidad
- :doc:`special-char` - Caracteres especiales
