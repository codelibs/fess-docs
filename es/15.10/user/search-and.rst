============
Búsqueda AND
============

Cuando desea buscar documentos que contengan todos los términos de búsqueda especificados, puede utilizar la búsqueda AND. Si escribe múltiples palabras separadas por espacios en el campo de entrada de búsqueda, por defecto se realizará una búsqueda AND, por lo que puede omitir AND y obtener el mismo resultado.

Cómo utilizar
-------------

Para utilizar la búsqueda AND, escriba AND entre los términos de búsqueda. AND
debe escribirse en mayúsculas y requiere espacios antes y después.
AND también se puede omitir.

Por ejemplo, si desea buscar documentos que contengan "Término1" y "Término2", ingrese lo siguiente en el formulario de búsqueda:

::

    Término1 AND Término2

Si omite AND y escribe de la siguiente manera, obtendrá el mismo resultado:

::

    Término1 Término2

También es posible conectar tres o más términos de búsqueda con AND.

::

    Término1 AND Término2 AND Término3

.. note::

    AND debe escribirse en mayúsculas. Si se escribe en minúsculas como ``and``, no se trata como un operador, sino que se busca como la palabra de búsqueda habitual "and". ``&&`` también se puede utilizar con el mismo significado que AND.

Utilizando paréntesis ``( )``, puede combinar la búsqueda AND con otras condiciones de búsqueda. Por ejemplo, si desea buscar documentos que contengan "Término1", y además contengan "Término2" o "Término3", ingrese lo siguiente:

::

    Término1 AND (Término2 OR Término3)

También es posible realizar una búsqueda AND especificando un campo. En el siguiente ejemplo, se buscan documentos que contengan "Término1" en el campo title, y "Término2" en el campo content.

::

    title:Término1 AND content:Término2
