======================
Búsqueda con comodines
======================

Puede utilizar comodines de un carácter o de varios caracteres dentro de los términos de búsqueda. ? se puede especificar como comodín de un carácter, y \* se puede especificar como comodín de varios caracteres. Los comodines se pueden utilizar en palabras. No es posible realizar búsquedas con comodines en oraciones.

Cómo utilizar
-------------

Para utilizar un comodín de un carácter, use ? de la siguiente manera:

::

    te?t

En el caso anterior, esto coincide con cualquier carácter individual en la posición de ?, como en text o test.

Para utilizar un comodín de varios caracteres, use \* de la siguiente manera:

::

    test*

En el caso anterior, esto coincide con cualquier cadena de cero o más caracteres en la posición de \*, como test, tests o tester. Además,

::

    te*t

también se puede utilizar en medio del término de búsqueda. Además,

::

    *test

también se puede utilizar un comodín al principio del término de búsqueda.

También puede realizar una búsqueda con comodines especificando un campo. En el siguiente ejemplo, se buscan documentos que contengan, en el campo title, una palabra que empiece por te y termine en t.

::

    title:te*t

Si no especifica ningún campo, la búsqueda se realiza sobre los campos title y content.

Condiciones de uso
------------------

Tenga en cuenta los siguientes puntos al utilizar la búsqueda con comodines.

* Los comodines coinciden con las cadenas de texto (tokens) registradas en el índice. Dado que el término de búsqueda no se vuelve a analizar, si el índice se crea con bi-gram u otros métodos, el japonés se trata como cadenas de longitud fija sin significado, por lo que los comodines en japonés no funcionarán como se espera. Si desea utilizar comodines en japonés, utilícelos en campos que usen análisis morfológico.
* Los patrones de comodines distinguen entre mayúsculas y minúsculas. Dado que las palabras registradas en el índice normalmente se convierten a minúsculas, utilice minúsculas en el patrón. Por ejemplo, ``Test*`` no coincide con ``test``, que se registra en minúsculas.
* Una búsqueda con un comodín al principio (por ejemplo, ``*test``) puede tardar en procesarse, ya que recorre todas las palabras del índice.
