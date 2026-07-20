============
Búsqueda NOT
============

Cuando desea buscar documentos que no contengan una palabra específica (búsqueda de exclusión), puede utilizar la búsqueda NOT. Es útil cuando desea excluir palabras clave concretas de los resultados de búsqueda para reducir el ruido.

Cómo utilizar
-------------

La búsqueda NOT se realiza agregando NOT antes de la palabra que no desea incluir. NOT
debe escribirse en mayúsculas y requiere espacios antes y después.

Por ejemplo, si desea buscar documentos que contengan "Término1" pero no contengan "Término2", ingrese lo siguiente y realice la búsqueda:

::

    Término1 NOT Término2

.. note::

    NOT debe escribirse en mayúsculas. Si se escribe en minúsculas como ``not``, no se trata como un operador, sino que se busca como la palabra de búsqueda habitual "not". Además, colocar ``-`` justo antes de la palabra que desea excluir, como en ``Término1 -Término2``, tiene el mismo significado que NOT.

Utilizando paréntesis ``( )``, puede combinar la búsqueda NOT con otras condiciones de búsqueda. Por ejemplo, si desea buscar documentos que contengan "Término1" o "Término2", pero no contengan "Término3", ingrese lo siguiente:

::

    (Término1 OR Término2) NOT Término3

También es posible realizar una búsqueda NOT especificando un campo. En el siguiente ejemplo, se buscan documentos que contengan "Término1" en el campo title, pero que no contengan "Término2" en el campo title.

::

    title:Término1 NOT title:Término2


Véase también
-------------

- :doc:`search-and` - Búsqueda AND
- :doc:`search-or` - Búsqueda OR
- :doc:`special-char` - Caracteres especiales
