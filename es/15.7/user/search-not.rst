===========
Búsqueda NOT
===========

Cuando desea buscar documentos que no contengan una palabra específica (búsqueda de exclusión), puede utilizar la búsqueda NOT. Es útil cuando desea excluir palabras clave concretas de los resultados de búsqueda para reducir el ruido.

Cómo utilizar
-------------

La búsqueda NOT se realiza agregando NOT antes de la palabra que no desea incluir. NOT
debe escribirse en mayúsculas y requiere espacios antes y después.

Por ejemplo, si desea buscar documentos que contengan "Término1" pero no contengan "Término2", ingrese lo siguiente y realice la búsqueda:

::

    Término1 NOT Término2

En lugar de NOT, también puede colocar ``-`` (guion) justo antes de la palabra que desea excluir. Lo siguiente tiene el mismo significado que el ejemplo anterior:

::

    Término1 -Término2


Véase también
-------------

- :doc:`search-and` - Búsqueda AND
- :doc:`search-or` - Búsqueda OR
- :doc:`special-char` - Caracteres especiales
