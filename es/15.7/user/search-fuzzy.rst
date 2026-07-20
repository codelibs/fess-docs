==============
Búsqueda difusa
==============

Búsqueda difusa (búsqueda aproximada)
======================================

Cuando desea buscar palabras que no coincidan exactamente con el término de búsqueda, puede utilizar la búsqueda difusa (búsqueda aproximada). Es útil cuando desea encontrar también documentos que no coinciden exactamente debido a errores de tecleo, variaciones en la escritura o diferencias de ortografía. |Fess| admite la búsqueda difusa (búsqueda aproximada) basada en la distancia de edición (distancia de Levenshtein), que indica cuánto difieren dos palabras entre sí.

Cómo utilizar
-------------

Para aplicar la búsqueda difusa, agregue "~" después del término de búsqueda.

Por ejemplo, si desea realizar una búsqueda difusa de la palabra "Fess", puede buscar documentos que contengan palabras similares a "Fess" (como "Fes") ingresando lo siguiente en el formulario de búsqueda:

::

    Fess~

El grado de tolerancia se puede especificar agregando un número del 0 al 2 después de ``~``. El número indica el límite superior de la distancia de edición permitida (el número máximo de inserciones, eliminaciones o sustituciones de caracteres); si se omite, se aplica la distancia de edición predeterminada.

::

    Fess~1
    Fess~2

Si especifica ``~2``, la búsqueda tolerará hasta 2 caracteres de diferencia respecto a ``Fess``.


Véase también
=============

- :doc:`search-wildcard` - Búsqueda con comodines
- :doc:`special-char` - Caracteres especiales

