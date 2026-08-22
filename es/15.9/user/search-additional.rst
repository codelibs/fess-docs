===============================
Condiciones de búsqueda ocultas
===============================

Puede utilizar el parámetro ``ex_q`` cuando desee transportar una condición de búsqueda específica sin mostrar su texto en la pantalla. Las condiciones especificadas en ``ex_q`` no se muestran en el campo de entrada de búsqueda y se conservan incluso cuando la pantalla se actualiza mediante la paginación o el filtrado por facetas.

En ``ex_q`` puede utilizar la misma sintaxis de consulta que en el término de búsqueda habitual (``q``): el formato ``field:value``, frases, especificaciones de rango, operadores como ``OR``, entre otros. La condición especificada se combina de forma predeterminada con la condición de ``q`` mediante AND al ejecutar la búsqueda. Es decir, los documentos que no coincidan con la condición de ``ex_q`` se excluyen de los resultados de búsqueda.

Cómo utilizar
-------------

Al ejecutar una búsqueda (por ejemplo, desde un formulario de búsqueda), agregue el valor de ``ex_q`` como campo de formulario oculto o como parámetro de consulta de la URL, y ejecute la búsqueda. Esto le permite buscar sin mostrar la condición en la pantalla.

Puede especificar ``ex_q`` varias veces. Como en el siguiente ejemplo, si pasa varios valores de ``ex_q``, cada uno se agrega como condición de búsqueda (los valores vacíos o duplicados se ignoran).

.. code-block:: none

    /search?q=keyword&ex_q=label:manual&ex_q=filetype:pdf

Conservación durante la paginación
-----------------------------------

Fess agrega automáticamente el valor de ``ex_q`` a los enlaces de paginación (como página siguiente y página anterior) y a los enlaces de filtrado por facetas. Por ello, la condición de ``ex_q`` se conserva incluso cuando la pantalla se actualiza mediante estas operaciones.

Por otro lado, si introduce una palabra clave en el campo de entrada de búsqueda estándar (el cuadro de búsqueda) y vuelve a buscar, ``ex_q`` no se traslada. Si desea que la condición se conserve también a través del cuadro de búsqueda, prepare un campo oculto ``ex_q`` en su propio formulario de búsqueda y envíe ``ex_q`` en cada búsqueda.

.. note::

    * Si la longitud de un valor individual de ``ex_q`` supera ``query.max.length`` (valor predeterminado: 1000 caracteres), ese valor se ignora sin generar un error.
    * ``ex_q`` puede utilizarse no solo en las búsquedas desde la pantalla web, sino también con la API de búsqueda (``/api/v2``). En la API se aplican el límite máximo de elementos ``ex_q`` por solicitud (``api.v2.param.max.array.size``, valor predeterminado: 100) y el límite máximo de longitud de cada elemento (``api.v2.param.max.length``, valor predeterminado: 1000 caracteres).
