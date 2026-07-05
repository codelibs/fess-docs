==============
Búsqueda difusa
==============

Búsqueda difusa (búsqueda aproximada)
======================================

Cuando desea buscar palabras que no coincidan exactamente con el término de búsqueda, puede utilizar la búsqueda difusa. |Fess| admite la búsqueda difusa (búsqueda aproximada) basada en la distancia de Levenshtein.

Cómo utilizar
-------------

Para aplicar la búsqueda difusa, agregue "~" después del término de búsqueda.

Por ejemplo, si desea realizar una búsqueda difusa de la palabra "Fess", puede buscar documentos que contengan palabras similares a "Fess" (como "Fes") ingresando lo siguiente en el formulario de búsqueda:

::

    Fess~

