==================
Búsqueda con boost
==================

Búsqueda con boost (búsqueda ponderada)
========================================

Cuando desea priorizar un término de búsqueda específico entre los términos de búsqueda, puede utilizar la búsqueda con boost. Al usar la búsqueda con boost, es posible buscar según la importancia de los términos de búsqueda.

Cómo utilizar
-------------

Para utilizar la búsqueda con boost, debe especificar el valor de boost (valor de ponderación) en el formato "^valor_de_boost" después del término de búsqueda.

Por ejemplo, si desea buscar "manzana naranja" pero priorizar las páginas que contengan más "manzana", ingrese lo siguiente en el formulario de búsqueda:

::

    manzana^100 naranja

El valor de boost debe ser un número entero mayor o igual a 1.
