==================
Búsqueda con boost
==================

Búsqueda con boost (búsqueda ponderada)
=======================================

Cuando desea priorizar un término de búsqueda específico entre los términos de búsqueda, puede utilizar la búsqueda con boost. Al usar la búsqueda con boost, es posible buscar según la importancia de los términos de búsqueda.

Cómo utilizar
-------------

Para utilizar la búsqueda con boost, debe especificar el valor de boost (valor de ponderación) en el formato "^valor_de_boost" inmediatamente después del término de búsqueda. No debe haber ningún espacio entre el término de búsqueda y el valor de boost.

Por ejemplo, si desea buscar "manzana naranja" pero quiere priorizar más "manzana", ingrese lo siguiente en el formulario de búsqueda:

::

    manzana^100 naranja

En este ejemplo, el valor de boost se aplica únicamente a "manzana" y no se aplica a "naranja".

Valor de boost
--------------

El valor de boost se especifica como un número. Puede indicar no solo números enteros, sino también decimales como ``2.5``.

- Si especifica un valor mayor que 1, el peso de ese término de búsqueda aumenta.
- Si especifica un valor mayor que 0 y menor que 1 (por ejemplo, ``0.5``), el peso de ese término de búsqueda disminuye.

El valor de boost no determina de forma absoluta la puntuación de los resultados de búsqueda, sino que ajusta el peso relativo respecto a otros términos de búsqueda.

Combinación con otra sintaxis de búsqueda
-----------------------------------------

La búsqueda con boost puede combinarse con otra sintaxis de búsqueda. Por ejemplo, también es posible añadir un valor de boost a un término de búsqueda que especifica un campo.

::

    title:manzana^100 naranja

En este ejemplo, se priorizan los documentos que contienen "manzana" en el campo title.
