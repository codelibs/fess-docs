===========
Búsqueda OR
===========

Cuando desea buscar documentos que contengan alguno de los términos de búsqueda, puede utilizar la búsqueda OR. Si escribe múltiples palabras en el campo de entrada de búsqueda, por defecto se realizará una búsqueda AND.

Cómo utilizar
-------------

Para utilizar la búsqueda OR, escriba OR entre los términos de búsqueda. OR
debe escribirse en mayúsculas y requiere espacios antes y después.

Por ejemplo, si desea buscar documentos que contengan "Término1" o "Término2", ingrese lo siguiente en el formulario de búsqueda:

::

    Término1 OR Término2

También es posible conectar tres o más términos de búsqueda con OR.

::

    Término1 OR Término2 OR Término3

.. note::

    OR debe escribirse en mayúsculas. Si se escribe en minúsculas como ``or``, no se trata como un operador, sino que se busca como la palabra de búsqueda habitual "or". ``||`` también se puede utilizar con el mismo significado que OR.

Utilizando paréntesis ``( )``, puede combinar la búsqueda OR con otras condiciones de búsqueda. Por ejemplo, si desea buscar documentos que contengan "Término1" o "Término2", y además contengan "Término3", ingrese lo siguiente:

::

    (Término1 OR Término2) Término3

También es posible realizar una búsqueda OR especificando un campo. En el siguiente ejemplo, se buscan documentos que contengan "Término1" en el campo title, o "Término2" en el campo content.

::

    title:Término1 OR content:Término2
